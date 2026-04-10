---
title: "Organizational and cultural gaps are more challenging than technical gaps for observability in distributed systems"
slug: organizational-gaps-outweigh-technical-gaps-observability
status: weakly_supported
confidence: 0.6
tags: [observability, organizational-challenges, distributed-systems, culture, monitoring]
domain: "ML Systems"
source_papers: [observability-monitoring-distributed-systems-industry-interview]
evidence:
  - source: observability-monitoring-distributed-systems-industry-interview
    type: supports
    strength: moderate
    detail: "28 industry interviews reveal that most participants consider culture and mindset challenges more difficult than technical challenges. Teams develop isolated monitoring without business context, and collaboration between teams is weakly pronounced. Participants describe missing strategy, roles, and responsibilities as root causes."
conditions: "Based on qualitative interviews in 2019, primarily with German/European organizations. Landscape may have shifted with DevOps and SRE maturation."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

In industry practice, organizational barriers -- including siloed team structures, lack of strategy and governance, missing roles and responsibilities, and insufficient awareness from both management and developers -- pose greater challenges to effective observability of distributed systems than purely technical limitations of monitoring tools.

## Evidence summary

Niedermaier et al. (2019) conducted 28 semi-structured interviews across 16 organizations. Multiple participants explicitly stated that culture and mindset aspects are more challenging than technical aspects. Challenges C3 (company culture), C4 (lack of central point of view), C6 (dependency on experts), C7 (lack of experience/time), and C8 (unclear non-functional requirements) are all fundamentally organizational rather than technical. The paper identifies governance (R5), collaboration model (R6), and monitoring mindset (R8) as key requirements that are organizational in nature.

## Conditions and scope

Claim is based on qualitative data from 2019. Since then, platform engineering and SRE adoption may have partially addressed organizational gaps. However, the fundamental tension between team autonomy (microservices/DevOps) and holistic observability likely persists.

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- Has the rise of platform engineering and dedicated SRE teams mitigated organizational observability gaps?
- Can organizational maturity for observability be measured quantitatively?
- Does the organizational-technical gap ratio differ by company size or industry sector?
