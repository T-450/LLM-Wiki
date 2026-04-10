---
title: "Fault Visibility Metric"
aliases: ["fault visibility", "fault coverage", "overall fault observability", "OFO", "fault observability metrics"]
tags: [observability, fault-detection, metrics, microservices, cloud-native]
maturity: emerging
key_papers: [informed-assessable-observability-design-decisions-cloud]
first_introduced: "Borges et al. (2024)"
date_updated: 2026-04-09
related_concepts: [distributed-tracing, observability-experiment]
---

## Definition

A set of three hierarchical metrics for quantifying the fault detection effectiveness of an observability configuration:

1. **Fault visibility** $v_{f,m,d} \in \{0,1\}$: whether fault $f$ is detectable in metric $m$ by detection mechanism $d$, i.e., $DF(m_t) > \alpha$
2. **Fault coverage** $FC_{f,d} = \frac{1}{n}\sum_{i=1}^{n} v_{f,m_i,d}$: fraction of collected metrics in which fault $f$ is visible
3. **Overall Fault Observability** $OFO_d = \frac{1}{l}\sum_{i=1}^{l} \mathbf{1}[FC_i > 0]$: fraction of all faults detectable in at least one metric

## Intuition

Analogous to test coverage in software testing: just as test coverage measures what fraction of code paths are exercised by tests, OFO measures what fraction of expected faults are observable in the current instrumentation configuration. A system with OFO=0.5 has 50% of known faults "invisible" — they would not trigger any detection mechanism, even if they occurred.

## Formal notation

Given a fault set $F = \{f_1, \ldots, f_l\}$, metric set $M = \{m_1, \ldots, m_n\}$, and detection mechanism $d$ with threshold $\alpha$:

$$v_{f,m,d} = \begin{cases} 1 & DF(m_t) > \alpha \\ 0 & \text{otherwise} \end{cases}$$

$$FC_{f,d} = \frac{1}{n}\sum_{i=1}^{n} v_{f,m_i,d}$$

$$OFO_d = \frac{1}{l}\sum_{i=1}^{l} \mathbf{1}\{FC_i > 0\}$$

## Variants

- Per-fault analysis: $v_{f,m,d}$ and $FC_{f,d}$ give fine-grained insight into which metrics are sensitive to which faults
- System-level summary: OFO provides a single number for overall observability quality
- Time-to-detect extension: incorporating MTTD as a continuous variant of the binary visibility score (proposed as future work)

## Comparison

| Metric | Granularity | Interpretability | Completeness |
|--------|------------|-----------------|--------------|
| MTTD (Mean Time To Detect) | System-level | High | Conflates many factors |
| MTTR | System-level | High | Broad, not specific to obs. config |
| Fault visibility ($v_{f,m,d}$) | Per fault-metric pair | High | Binary only |
| Fault coverage ($FC_{f,d}$) | Per fault | Medium | Depends on metric set |
| OFO | System-level | High | Depends on fault set completeness |

## When to use

- When comparing two or more observability configurations empirically
- When deciding which instrumentation to add or which sampling parameters to tune
- When auditing an existing observability setup to find invisible fault classes
- As a continuous metric in CI/CD pipelines for observability assurance

## Known limitations

- Binary visibility score may oversimplify — borderline detections near threshold $\alpha$ contribute the same as clearly visible faults
- OFO depends on the completeness and representativeness of the fault set $F$; unknown fault types are not covered
- Detection mechanism $d$ must be selected and tuned; the metrics combine observability quality and detector quality

## Open problems

- Extending to continuous (non-binary) visibility scores
- Automatically generating comprehensive fault sets for OFO evaluation
- Incorporating log-based observability into the metric framework

## Key papers

- [[informed-assessable-observability-design-decisions-cloud]] — introduces and validates the fault visibility metric framework with the OXN tool

## My understanding

A principled and practically useful formalization. The test-coverage analogy is apt and communicable to engineering teams. The main weakness is the binary visibility score — a fault barely above/below the threshold contributes equally to OFO. Future work on continuous scores and automated fault set generation would strengthen the framework considerably.
