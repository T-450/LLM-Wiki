---
title: "SLO-based alerting detects partial failures missed by threshold monitoring"
slug: slo-based-alerting-detects-partial-failures
status: weakly_supported
confidence: 0.65
tags: [observability, slo, alerting, monitoring, reliability]
domain: "ML Systems"
source_papers: [observability-engineering-majors-fong-jones-miranda, monitoring-distributed-systems-google-sre]
evidence:
  - source: observability-engineering-majors-fong-jones-miranda
    type: supports
    strength: moderate
    detail: "Case study: Honeycomb detected a user-impacting brownout via SLO burn rate alert while all threshold-based monitors showed green. Event-based SLIs captured the fraction of failing requests; time-based uptime metrics did not."
  - source: monitoring-distributed-systems-google-sre
    type: supports
    strength: weak
    detail: "Argues symptom-based alerting (SLO-style) is more reliable than cause-based threshold alerting; advocates for monitoring user-visible impact over internal resource metrics."
conditions: "Claim applies when partial failures affect a subset of requests (e.g., 5% error rate) while overall system uptime remains 100%. Traditional uptime-based monitoring cannot detect this; event-based SLIs can."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

SLO-based alerting using event-based SLIs detects partial service failures (affecting a fraction of users) that threshold-based and uptime-based monitoring systems miss entirely. This is because SLOs measure user-visible impact directly, whereas threshold monitors measure internal resource state that may be uncorrelated with user experience.

## Evidence summary

One practitioner case study (Honeycomb incident documented in [[observability-engineering-majors-fong-jones-miranda]]) provides direct support: SLO burn rate fired, all other monitors showed green. The [[monitoring-distributed-systems-google-sre]] SRE book argues the same point theoretically via the symptom vs. cause monitoring distinction. Both are practitioner evidence rather than controlled experiments.

## Conditions and scope

- Applies to partial failures (e.g., 5-20% error rate) — total outages are detected by both approaches
- Requires event-based SLI infrastructure (structured events with consistent request counting)
- Time-based SLIs (uptime) do NOT provide this advantage; event-based SLIs are the key

## Counter-evidence

No published counter-evidence. However, poorly set SLO thresholds can produce the same alert fatigue as threshold monitoring — the claim holds only when SLOs are well-calibrated.

## Linked ideas

- [[slo-driven-observability-configuration-optimizer]] — addresses the open problem of automatically optimizing observability configuration to support SLO detection

## Open questions

- What is the minimum event volume needed for SLI statistical validity in low-traffic services?
- How should SLO thresholds be automatically calibrated from historical traffic?
