---
title: "ML-based anomaly detection accuracy degrades under service evolution, requiring costly retraining"
slug: ml-retraining-cost-accuracy-tradeoff
status: weakly_supported
confidence: 0.65
tags: [anomaly-detection, machine-learning, concept-drift, retraining, microservices]
domain: "ML Systems"
source_papers: [anomaly-detection-failure-root-cause-analysis]
evidence:
  - source: anomaly-detection-failure-root-cause-analysis
    type: supports
    strength: moderate
    detail: "Survey identifies that ML models for anomaly detection and RCA lose accuracy when services or runtime environments change, requiring time-consuming retraining. The survey discusses this as a fundamental tension: modern CI/CD means continuous changes, but retraining is not suited for continuous execution."
conditions: "Applies to supervised and unsupervised ML approaches trained on static baselines; continual learning methods may mitigate this."
date_proposed: 2026-04-09
date_updated: 2026-04-09
---

## Statement

Machine learning-based anomaly detection techniques for microservice applications experience accuracy degradation when the services forming an application or their runtime conditions change over time. Retraining models to restore accuracy is time-consuming and operationally costly, creating a fundamental tradeoff between update frequency and detection accuracy in continuously evolving systems.

## Evidence summary

The Soldani & Brogi (2022) survey discusses that techniques like Seer, DLA, and workflow-aware fault diagnosis require model retraining when application topology or behavior changes. The survey notes that modern continuous delivery practices mean services are continuously updated, creating a mismatch with static ML baselines. Some techniques (e.g., Brandon et al.) require manual artifact updates from operators. The survey proposes continual learning as a potential research direction to address this.

## Conditions and scope

Most relevant to statically-trained models. Online learning and continual learning approaches may partially address this, though they introduce their own challenges (catastrophic forgetting, computational overhead).

## Counter-evidence

None documented yet.

## Linked ideas

## Open questions

- Can continual learning effectively maintain anomaly detection accuracy without full retraining?
- What is the empirical relationship between service update frequency and model accuracy degradation?
- Are there lightweight model adaptation techniques that avoid full retraining?
