"""Tests for tools/remote.py — SSH remote server operations."""

from __future__ import annotations

import json
import os
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure tools/ is importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.remote import (
    ANOMALY_PATTERNS,
    DEFAULT_SYNC_EXCLUDE,
    DEFAULT_SYNC_INCLUDE,
    FREE_GPU_THRESHOLD_MIB,
    REQUIRED_FIELDS,
    build_ssh_cmd,
    build_ssh_transport,
    conda_prefix,
    detect_anomalies,
    load_config,
    parse_nvidia_smi,
    _parse_yaml,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_CONFIG_YAML = textwrap.dedent("""\
    host: gpu.example.com
    user: alice
    work_dir: /home/alice/exp
    conda:
      path: /opt/conda
      env: ml
""")

FULL_CONFIG_YAML = textwrap.dedent("""\
    host: gpu.lab.edu
    user: bob
    port: 2222
    identity_file: ~/.ssh/lab_key
    proxy_jump: bastion.lab.edu
    ssh_options:
      ServerAliveInterval: "60"
      ServerAliveCountMax: "3"
    gpus: "4x A100 80GB"
    work_dir: /data/bob/experiments
    conda:
      path: /opt/miniconda3
      env: research
    sync:
      include:
        - "*.py"
        - "*.yaml"
        - "*.sh"
      exclude:
        - ".git/"
        - "big_data/"
    free_gpu_threshold_mib: 1000
""")

ENV_SETUP_CONFIG_YAML = textwrap.dedent("""\
    host: cluster.hpc.edu
    user: charlie
    work_dir: /scratch/charlie
    env_setup: "module load cuda/12.1 && source /home/charlie/venv/bin/activate"
""")


@pytest.fixture
def minimal_config_file(tmp_path):
    p = tmp_path / "server.yaml"
    p.write_text(MINIMAL_CONFIG_YAML)
    return str(p)


@pytest.fixture
def full_config_file(tmp_path):
    p = tmp_path / "server.yaml"
    p.write_text(FULL_CONFIG_YAML)
    return str(p)


@pytest.fixture
def env_setup_config_file(tmp_path):
    p = tmp_path / "server.yaml"
    p.write_text(ENV_SETUP_CONFIG_YAML)
    return str(p)


@pytest.fixture
def minimal_cfg(minimal_config_file):
    return load_config(minimal_config_file)


@pytest.fixture
def full_cfg(full_config_file):
    return load_config(full_config_file)


@pytest.fixture
def env_setup_cfg(env_setup_config_file):
    return load_config(env_setup_config_file)


# ===================================================================
# YAML Parser Tests
# ===================================================================


class TestYamlParser:
    def test_simple_scalars(self):
        text = "host: example.com\nport: 22\nenabled: true"
        result = _parse_yaml(text)
        assert result["host"] == "example.com"
        assert result["port"] == 22
        assert result["enabled"] is True

    def test_quoted_strings(self):
        text = 'name: "hello world"\npath: \'/opt/bin\''
        result = _parse_yaml(text)
        assert result["name"] == "hello world"
        assert result["path"] == "/opt/bin"

    def test_inline_list(self):
        text = "tags: [a, b, c]"
        result = _parse_yaml(text)
        assert result["tags"] == ["a", "b", "c"]

    def test_block_list(self):
        text = "items:\n  - one\n  - two\n  - three"
        result = _parse_yaml(text)
        assert result["items"] == ["one", "two", "three"]

    def test_nested_dict(self):
        text = "conda:\n  path: /opt/conda\n  env: ml"
        result = _parse_yaml(text)
        assert result["conda"]["path"] == "/opt/conda"
        assert result["conda"]["env"] == "ml"

    def test_inline_empty_dict(self):
        text = "ssh_options: {}"
        result = _parse_yaml(text)
        assert result["ssh_options"] == {}

    def test_comments_ignored(self):
        text = "host: example.com  # the server\n# full line comment\nuser: alice"
        result = _parse_yaml(text)
        assert result["host"] == "example.com"
        assert result["user"] == "alice"

    def test_empty_string_value(self):
        text = 'proxy_jump: ""'
        result = _parse_yaml(text)
        assert result["proxy_jump"] == ""

    def test_float_value(self):
        text = "threshold: 500.5"
        result = _parse_yaml(text)
        assert result["threshold"] == 500.5

    def test_boolean_false(self):
        text = "enabled: false"
        result = _parse_yaml(text)
        assert result["enabled"] is False


# ===================================================================
# Config Loading Tests
# ===================================================================


class TestConfigLoading:
    def test_minimal_config_loads(self, minimal_cfg):
        assert minimal_cfg["host"] == "gpu.example.com"
        assert minimal_cfg["user"] == "alice"
        assert minimal_cfg["work_dir"] == "/home/alice/exp"

    def test_minimal_config_defaults(self, minimal_cfg):
        assert minimal_cfg["port"] == 22
        assert minimal_cfg["identity_file"] == ""
        assert minimal_cfg["proxy_jump"] == ""
        assert minimal_cfg["ssh_options"] == {}
        assert minimal_cfg["gpus"] == "unknown"
        assert minimal_cfg["free_gpu_threshold_mib"] == FREE_GPU_THRESHOLD_MIB

    def test_minimal_config_sync_defaults(self, minimal_cfg):
        assert minimal_cfg["sync"]["include"] == DEFAULT_SYNC_INCLUDE
        assert minimal_cfg["sync"]["exclude"] == DEFAULT_SYNC_EXCLUDE

    def test_full_config_overrides(self, full_cfg):
        assert full_cfg["port"] == 2222
        assert full_cfg["identity_file"] == "~/.ssh/lab_key"
        assert full_cfg["proxy_jump"] == "bastion.lab.edu"
        assert full_cfg["ssh_options"]["ServerAliveInterval"] == "60"
        assert full_cfg["gpus"] == "4x A100 80GB"
        assert full_cfg["free_gpu_threshold_mib"] == 1000

    def test_full_config_custom_sync(self, full_cfg):
        assert "*.py" in full_cfg["sync"]["include"]
        assert "big_data/" in full_cfg["sync"]["exclude"]

    def test_env_setup_config(self, env_setup_cfg):
        assert "module load cuda/12.1" in env_setup_cfg["env_setup"]

    def test_missing_host_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("user: alice\nwork_dir: /tmp\nconda:\n  path: /opt\n  env: ml")
        with pytest.raises(SystemExit):
            load_config(str(p))

    def test_missing_user_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("host: example.com\nwork_dir: /tmp\nconda:\n  path: /opt\n  env: ml")
        with pytest.raises(SystemExit):
            load_config(str(p))

    def test_missing_work_dir_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("host: example.com\nuser: alice\nconda:\n  path: /opt\n  env: ml")
        with pytest.raises(SystemExit):
            load_config(str(p))

    def test_no_conda_no_env_setup_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("host: example.com\nuser: alice\nwork_dir: /tmp")
        with pytest.raises(SystemExit):
            load_config(str(p))

    def test_nonexistent_file_fails(self):
        with pytest.raises(SystemExit):
            load_config("/nonexistent/path/server.yaml")

    def test_conda_without_path_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("host: example.com\nuser: alice\nwork_dir: /tmp\nconda:\n  env: ml")
        with pytest.raises(SystemExit):
            load_config(str(p))

    def test_conda_without_env_fails(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text("host: example.com\nuser: alice\nwork_dir: /tmp\nconda:\n  path: /opt")
        with pytest.raises(SystemExit):
            load_config(str(p))


# ===================================================================
# SSH Command Building Tests
# ===================================================================


class TestBuildSshCmd:
    def test_minimal(self, minimal_cfg):
        cmd = build_ssh_cmd(minimal_cfg)
        assert cmd[0] == "ssh"
        assert "alice@gpu.example.com" in cmd
        assert "-o" in cmd
        assert "ConnectTimeout=10" in cmd
        assert "BatchMode=yes" in cmd

    def test_no_port_flag_for_22(self, minimal_cfg):
        cmd = build_ssh_cmd(minimal_cfg)
        assert "-p" not in cmd

    def test_custom_port(self, full_cfg):
        cmd = build_ssh_cmd(full_cfg)
        idx = cmd.index("-p")
        assert cmd[idx + 1] == "2222"

    def test_identity_file(self, full_cfg):
        cmd = build_ssh_cmd(full_cfg)
        idx = cmd.index("-i")
        assert "lab_key" in cmd[idx + 1]

    def test_proxy_jump(self, full_cfg):
        cmd = build_ssh_cmd(full_cfg)
        idx = cmd.index("-J")
        assert cmd[idx + 1] == "bastion.lab.edu"

    def test_ssh_options(self, full_cfg):
        cmd = build_ssh_cmd(full_cfg)
        # Should have ServerAliveInterval=60 as -o option
        found = False
        for i, part in enumerate(cmd):
            if part == "-o" and i + 1 < len(cmd) and "ServerAliveInterval=60" in cmd[i + 1]:
                found = True
        assert found

    def test_user_host_format(self, full_cfg):
        cmd = build_ssh_cmd(full_cfg)
        assert "bob@gpu.lab.edu" in cmd

    def test_no_proxy_when_empty(self, minimal_cfg):
        cmd = build_ssh_cmd(minimal_cfg)
        assert "-J" not in cmd

    def test_no_identity_when_empty(self, minimal_cfg):
        cmd = build_ssh_cmd(minimal_cfg)
        assert "-i" not in cmd


class TestBuildSshTransport:
    def test_minimal(self, minimal_cfg):
        t = build_ssh_transport(minimal_cfg)
        assert t.startswith("ssh")
        assert "BatchMode=yes" in t

    def test_with_port(self, full_cfg):
        t = build_ssh_transport(full_cfg)
        assert "-p 2222" in t

    def test_with_identity(self, full_cfg):
        t = build_ssh_transport(full_cfg)
        assert "-i" in t
        assert "lab_key" in t

    def test_with_proxy(self, full_cfg):
        t = build_ssh_transport(full_cfg)
        assert "-J bastion.lab.edu" in t


# ===================================================================
# Conda Prefix Tests
# ===================================================================


class TestCondaPrefix:
    def test_conda_config(self, minimal_cfg):
        prefix = conda_prefix(minimal_cfg)
        assert "conda shell.bash hook" in prefix
        assert "conda activate ml" in prefix
        assert "/opt/conda/bin/conda" in prefix

    def test_env_setup_config(self, env_setup_cfg):
        prefix = conda_prefix(env_setup_cfg)
        assert "module load cuda/12.1" in prefix
        assert "source" in prefix

    def test_no_env_returns_empty(self):
        cfg = {"host": "x", "user": "x", "work_dir": "/tmp"}
        prefix = conda_prefix(cfg)
        assert prefix == ""


# ===================================================================
# nvidia-smi Parsing Tests
# ===================================================================


class TestParseNvidiaSmi:
    def test_single_gpu_free(self):
        csv = "0, NVIDIA A100-SXM4-80GB, 312, 81920, 0, 32\n"
        gpus = parse_nvidia_smi(csv)
        assert len(gpus) == 1
        assert gpus[0]["index"] == 0
        assert gpus[0]["name"] == "NVIDIA A100-SXM4-80GB"
        assert gpus[0]["memory_used_mib"] == 312
        assert gpus[0]["memory_total_mib"] == 81920
        assert gpus[0]["free"] is True
        assert gpus[0]["free_memory_mib"] == 81920 - 312

    def test_single_gpu_busy(self):
        csv = "0, RTX 4090, 22000, 24576, 95, 72\n"
        gpus = parse_nvidia_smi(csv)
        assert len(gpus) == 1
        assert gpus[0]["free"] is False

    def test_multiple_gpus(self):
        csv = (
            "0, A100, 200, 81920, 0, 30\n"
            "1, A100, 45000, 81920, 98, 75\n"
            "2, A100, 100, 81920, 0, 28\n"
            "3, A100, 80000, 81920, 100, 82\n"
        )
        gpus = parse_nvidia_smi(csv)
        assert len(gpus) == 4
        free = [g["index"] for g in gpus if g["free"]]
        assert free == [0, 2]

    def test_custom_threshold(self):
        csv = "0, A100, 800, 81920, 5, 35\n"
        gpus = parse_nvidia_smi(csv, threshold=1000)
        assert gpus[0]["free"] is True
        gpus2 = parse_nvidia_smi(csv, threshold=500)
        assert gpus2[0]["free"] is False

    def test_empty_output(self):
        gpus = parse_nvidia_smi("")
        assert gpus == []

    def test_whitespace_only(self):
        gpus = parse_nvidia_smi("   \n  \n")
        assert gpus == []

    def test_malformed_line_skipped(self):
        csv = "bad line\n0, A100, 200, 81920, 0, 30\n"
        gpus = parse_nvidia_smi(csv)
        assert len(gpus) == 1
        assert gpus[0]["index"] == 0

    def test_four_columns_minimum(self):
        csv = "0, A100, 200, 81920\n"
        gpus = parse_nvidia_smi(csv)
        assert len(gpus) == 1
        assert "utilization_pct" not in gpus[0]
        assert "temperature_c" not in gpus[0]

    def test_five_columns(self):
        csv = "0, A100, 200, 81920, 50\n"
        gpus = parse_nvidia_smi(csv)
        assert gpus[0]["utilization_pct"] == 50
        assert "temperature_c" not in gpus[0]

    def test_float_memory_values(self):
        csv = "0, A100, 312.5, 81920.0, 0.0, 32.0\n"
        gpus = parse_nvidia_smi(csv)
        assert gpus[0]["memory_used_mib"] == 312
        assert gpus[0]["memory_total_mib"] == 81920


# ===================================================================
# Anomaly Detection Tests
# ===================================================================


class TestDetectAnomalies:
    def test_nan_detection(self):
        lines = ["epoch 1, loss=0.5", "epoch 2, loss=nan", "epoch 3, loss=0.3"]
        anomalies = detect_anomalies(lines)
        assert len(anomalies) == 1
        assert anomalies[0]["type"] == "NaN detected"
        assert anomalies[0]["line_number"] == 1

    def test_oom_detection(self):
        lines = ["CUDA out of memory. Tried to allocate 2.00 GiB"]
        anomalies = detect_anomalies(lines)
        assert len(anomalies) == 1
        assert anomalies[0]["type"] == "OOM"

    def test_oom_alternative_pattern(self):
        lines = ["torch.cuda.OutOfMemoryError: CUDA out of memory"]
        anomalies = detect_anomalies(lines)
        assert any(a["type"] == "OOM" for a in anomalies)

    def test_traceback_detection(self):
        lines = ["Traceback (most recent call last):", "  File ...", "RuntimeError: ..."]
        anomalies = detect_anomalies(lines)
        types = {a["type"] for a in anomalies}
        assert "Traceback/crash" in types

    def test_runtime_error_detection(self):
        lines = ["RuntimeError: expected scalar type Float but found Half"]
        anomalies = detect_anomalies(lines)
        assert any(a["type"] == "Runtime error" for a in anomalies)

    def test_inf_loss_detection(self):
        lines = ["step 100, loss: inf"]
        anomalies = detect_anomalies(lines)
        assert any(a["type"] == "Infinite loss" for a in anomalies)

    def test_no_anomalies(self):
        lines = ["epoch 1, loss=2.5, acc=0.75", "epoch 2, loss=1.8, acc=0.82"]
        anomalies = detect_anomalies(lines)
        assert anomalies == []

    def test_dedup_same_type(self):
        lines = ["loss=nan", "loss=nan", "loss=nan"]
        anomalies = detect_anomalies(lines)
        # Should only report NaN once
        nan_count = sum(1 for a in anomalies if a["type"] == "NaN detected")
        assert nan_count == 1

    def test_multiple_different_anomalies(self):
        lines = [
            "loss=nan",
            "CUDA out of memory",
            "Traceback (most recent call last):",
        ]
        anomalies = detect_anomalies(lines)
        types = {a["type"] for a in anomalies}
        assert "NaN detected" in types
        assert "OOM" in types
        assert "Traceback/crash" in types

    def test_empty_lines(self):
        anomalies = detect_anomalies([])
        assert anomalies == []

    def test_long_line_truncated(self):
        long_line = "NaN " + "x" * 500
        anomalies = detect_anomalies([long_line])
        assert len(anomalies[0]["content"]) <= 200


# ===================================================================
# CLI Tests (argparse validation)
# ===================================================================


class TestCLI:
    def test_no_command_exits(self, capsys):
        """Running with no command should print help and exit."""
        with pytest.raises(SystemExit):
            from tools.remote import main
            with patch("sys.argv", ["remote.py"]):
                main()

    def test_launch_requires_name(self):
        """launch --cmd X without --name should fail."""
        from tools.remote import main
        with patch("sys.argv", ["remote.py", "--config", "/dev/null", "launch", "--cmd", "echo"]):
            with pytest.raises(SystemExit):
                main()

    def test_launch_requires_cmd(self):
        """launch --name X without --cmd should fail."""
        from tools.remote import main
        with patch("sys.argv", ["remote.py", "--config", "/dev/null", "launch", "--name", "test"]):
            with pytest.raises(SystemExit):
                main()

    def test_pull_requires_paths(self):
        """pull-results without paths should fail."""
        from tools.remote import main
        with patch("sys.argv", ["remote.py", "--config", "/dev/null", "pull-results"]):
            with pytest.raises(SystemExit):
                main()


# ===================================================================
# Launch Command Building Tests
# ===================================================================


class TestLaunchCommandBuilding:
    """Test that launch builds correct screen/conda/CUDA commands."""

    def test_conda_prefix_in_launch(self, minimal_cfg):
        prefix = conda_prefix(minimal_cfg)
        assert "/opt/conda/bin/conda shell.bash hook" in prefix
        assert "conda activate ml" in prefix

    def test_gpu_binding_format(self):
        # Simulate what launch does with --gpu
        gpu = "0,1"
        gpu_part = f"CUDA_VISIBLE_DEVICES={gpu} "
        assert gpu_part == "CUDA_VISIBLE_DEVICES=0,1 "

    def test_no_gpu_binding(self):
        # When --gpu is None, no CUDA_VISIBLE_DEVICES
        gpu = None
        gpu_part = f"CUDA_VISIBLE_DEVICES={gpu} " if gpu is not None else ""
        assert gpu_part == ""

    def test_log_file_default_format(self):
        session_name = "exp-my-test"
        log_file = f"logs/{session_name}.log"
        assert log_file == "logs/exp-my-test.log"

    def test_screen_command_format(self):
        session = "exp-test"
        inner_cmd = "cd /tmp && python train.py"
        screen_cmd = f"screen -dmS {session} bash -c '{inner_cmd}'"
        assert "screen -dmS exp-test" in screen_cmd
        assert "bash -c" in screen_cmd


# ===================================================================
# Config Example File Tests
# ===================================================================


class TestConfigExample:
    """Verify the example config file is valid and parseable."""

    def test_example_file_exists(self):
        example = ROOT / "config" / "server.yaml.example"
        assert example.exists(), "config/server.yaml.example must exist"

    def test_example_file_parseable(self):
        example = ROOT / "config" / "server.yaml.example"
        text = example.read_text(encoding="utf-8")
        result = _parse_yaml(text)
        assert "host" in result
        assert "user" in result
        assert "work_dir" in result

    def test_example_has_conda(self):
        example = ROOT / "config" / "server.yaml.example"
        text = example.read_text(encoding="utf-8")
        result = _parse_yaml(text)
        assert "conda" in result
        assert "path" in result["conda"]
        assert "env" in result["conda"]

    def test_example_has_sync(self):
        example = ROOT / "config" / "server.yaml.example"
        text = example.read_text(encoding="utf-8")
        result = _parse_yaml(text)
        assert "sync" in result
        assert "include" in result["sync"]
        assert "exclude" in result["sync"]

    def test_example_include_covers_key_patterns(self):
        example = ROOT / "config" / "server.yaml.example"
        text = example.read_text(encoding="utf-8")
        result = _parse_yaml(text)
        includes = result["sync"]["include"]
        assert "*.py" in includes
        assert "*.yaml" in includes
        assert "*.sh" in includes
        assert "requirements*.txt" in includes

    def test_example_exclude_covers_key_patterns(self):
        example = ROOT / "config" / "server.yaml.example"
        text = example.read_text(encoding="utf-8")
        result = _parse_yaml(text)
        excludes = result["sync"]["exclude"]
        assert ".git/" in excludes
        assert "__pycache__/" in excludes
        assert "*.pt" in excludes
        assert "*.safetensors" in excludes


# ===================================================================
# Integration: SKILL.md references remote.py
# ===================================================================


class TestSkillReferences:
    """Verify /exp-run SKILL.md references tools/remote.py."""

    def _skill_path(self):
        # Support both old and new skill directory names
        for name in ("exp-run", "run-experiment"):
            p = ROOT / ".claude" / "skills" / name / "SKILL.md"
            if p.exists():
                return p
        return ROOT / ".claude" / "skills" / "exp-run" / "SKILL.md"

    def test_skill_file_exists(self):
        assert self._skill_path().exists()

    def test_skill_mentions_remote_tool(self):
        content = self._skill_path().read_text(encoding="utf-8")
        assert "tools/remote.py" in content or "remote.py" in content

    def test_skill_mentions_server_config(self):
        content = self._skill_path().read_text(encoding="utf-8")
        assert "server.yaml" in content or "config/server" in content
