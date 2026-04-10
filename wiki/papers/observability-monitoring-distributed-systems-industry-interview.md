---
title: "On Observability and Monitoring of Distributed Systems -- An Industry Interview Study"
slug: observability-monitoring-distributed-systems-industry-interview
arxiv: "1907.12240"
venue: "ICSOC"
year: 2019
tags: [observability, monitoring, distributed-systems, microservices, qualitative-study, industry, cloud, DevOps]
importance: 3
date_added: 2026-04-09
source_type: tex
s2_id: ""
keywords: [observability, monitoring, distributed systems, cloud, microservices, industry interview, organizational challenges, distributed tracing]
domain: "ML Systems"
code_url: ""
cited_by: []
---

## Problem

Modern distributed systems built with microservices, cloud deployments, and DevOps practices have growing complexity that outpaces the capabilities of existing monitoring tools. While these paradigms enable faster delivery and independent development cycles, they create significant operational challenges: service interdependencies are poorly understood, monitoring is implemented reactively rather than systematically, and organizational silos prevent holistic observability. There is no research matching new monitoring solutions and technologies to the specific challenges companies face in practice.

## Key idea

A qualitative industry study based on 28 semi-structured interviews with software professionals across 16 organizations reveals that monitoring and observability of distributed systems is not purely a technical problem but a cross-cutting strategic concern. The study identifies 9 challenges (including increasing dynamics/complexity, heterogeneity, company culture/mindset, lack of central point of view, data flood, expert dependency), 14 requirements (holistic approach, business-centric management, context propagation, governance, collaboration model, monitoring platform, monitoring mindset, etc.), and maps them to existing solutions (event management, distributed tracing, SRE/SLO, APM, AI-based anomaly detection). The core finding is that organizational aspects -- strategy, roles, responsibilities, and cultural awareness -- are at least as challenging as the technical aspects of monitoring.

## Method

1. Applied five-step case study research process (Runeson & Hoest) with three research questions: contemporary challenges (RQ1), stakeholder requirements (RQ2), and organizational/technical solutions (RQ3)
2. Conducted 28 semi-structured interviews (45 min average) between Feb-Apr 2019 across 16 organizations spanning IoT, telecom, insurance, IT consulting, tool providers, and applied research
3. Covered diverse roles: DevOps engineers, product owners, service managers, architects, consultants, CTOs
4. Applied Mayring's qualitative content analysis with inductive category development on sentence-level coding
5. Transcripts reviewed by multiple researchers; participants reviewed and corrected their transcripts

## Results

- **9 challenges identified**: (C1) increasing dynamics and complexity, (C2) heterogeneity across layers and teams, (C3) company culture and mindset barriers, (C4) lack of central point of view, (C5) flood of data, (C6) dependency on individual experts, (C7) lack of experience/time/resources, (C8) unclear non-functional requirements, (C9) reactive implementation
- **Key organizational finding**: culture and mindset challenges (C3) were considered more difficult than technical challenges by most participants; teams develop isolated monitoring without business context
- **Distributed tracing recognized but underutilized**: participants highlighted distributed tracing (S3) as a key solution for holistic views, but instrumentation is not consistently assured across teams
- **AI/ML preconditions unmet**: participants acknowledged AI potential for anomaly detection but noted that preconditions (right data, quality, context, central storage) are still missing in practice; concerns about cost-value ratio and reliability
- **SRE and SLO adoption growing**: several companies adopting Site Reliability Engineering and Service Level Objectives to align business goals with technical metrics
- **14 requirements mapped to solutions**: challenges, requirements, and solutions form an interconnected matrix showing how organizational and technical measures address multiple challenges simultaneously

## Limitations

- Qualitative study; results are not statistically generalizable
- Interviews conducted primarily with German-based companies (though from international organizations)
- Interviews from 2019; the observability landscape has evolved (OpenTelemetry, eBPF)
- Does not evaluate effectiveness of proposed solutions, only documents their use
- No follow-up longitudinal assessment of whether identified challenges were resolved

## Open questions

- Has OpenTelemetry adoption since 2019 resolved the instrumentation consistency challenge identified in this study?
- How have organizational structures for observability evolved -- do dedicated observability teams now exist more broadly?
- What quantitative evidence exists for the claim that organizational factors outweigh technical factors in observability effectiveness?
- Can the challenges-requirements-solutions mapping be formalized into an actionable maturity model?

## My take

An important empirical grounding for the observability research space. While primarily qualitative and now somewhat dated (pre-OpenTelemetry maturity), the core finding -- that organizational and cultural barriers are more challenging than technical ones -- remains highly relevant. The paper provides the practitioner perspective that complements the more technically-focused surveys like Soldani & Brogi (2022). The challenge taxonomy (C1-C9) is a useful reference frame for positioning subsequent technical work. The finding that AI preconditions are unmet in practice is a valuable reality check for the AIOps research community.

## Related

- [[observability-foundations-distributed-systems]]
- [[observability-engineering-tooling]]
- [[distributed-tracing]]
- [[monitoring-complexity-gap-distributed-systems]]
- supports: [[organizational-gaps-outweigh-technical-gaps-observability]]
- supports: [[distributed-tracing-adoption-gap-industry]]
- supports: [[ai-prerequisites-unmet-observability-practice]]
