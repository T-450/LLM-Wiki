---
title: "Consensus and Coordination in Distributed Systems"
tags: [consensus, distributed-systems, raft, paxos, coordination, leader-election]
my_involvement: reading
sota_updated: 2026-04-09
key_venues: [OSDI, SOSP, EuroSys, NSDI, VLDB]
related_topics:
  - fault-tolerance-reliability
  - distributed-storage-databases
  - observability-foundations-distributed-systems
key_people: []
---

## Overview

Consensus is the fundamental problem of getting a group of distributed processes to agree on a value despite failures and network partitions. It underpins virtually every reliable distributed system — from replicated databases to distributed locking services to leader election in clustered applications.

The core challenge is captured by the FLP impossibility result (Fischer, Lynch, Paterson 1985): no deterministic algorithm can solve consensus in an asynchronous system if even one process may fail. Practical systems work around this by using timeouts, randomization, or relaxing assumptions (e.g., synchrony bounds in Paxos and Raft).

Key systems and algorithms: **Paxos** (Lamport 1989/2001), **Multi-Paxos**, **Raft** (Ongaro & Ousterhout 2014), **Viewstamped Replication**, **Zab** (ZooKeeper Atomic Broadcast), **PBFT** (Byzantine fault tolerance).

## Timeline

- **1978**: Lamport's logical clocks establish happens-before ordering
- **1985**: FLP impossibility result published
- **1989/2001**: Paxos algorithm described (Lamport)
- **2007**: Zab protocol deployed in ZooKeeper (Yahoo)
- **2012**: Spanner: globally distributed, strongly consistent database (Google)
- **2014**: Raft algorithm — designed for understandability (Ongaro & Ousterhout)
- **2020s**: Flexible Paxos, EPaxos, and variants for geo-distributed deployments

## Seminal works

- Lamport, "The Part-Time Parliament" (Paxos, 1998/2001)
- Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (Raft, USENIX ATC 2014)
- Fischer, Lynch, Paterson, "Impossibility of Distributed Consensus with One Faulty Process" (1985)
- Corbett et al., "Spanner: Google's Globally Distributed Database" (OSDI 2012)
- Castro & Liskov, "Practical Byzantine Fault Tolerance" (OSDI 1999)

## SOTA tracker

| System / Algorithm | Venue | Year | Notes |
|---|---|---|---|
| Raft | USENIX ATC | 2014 | De facto standard for new systems; used in etcd, CockroachDB, TiKV |
| EPaxos | SOSP | 2013 | Leaderless, lower latency in geo-distributed settings |
| Flexible Paxos | arXiv | 2016 | Quorum size can vary per phase |
| HotStuff | PODC | 2019 | Linear complexity BFT, used in Diem/LibraBFT |

## Open problems

- Reducing latency in WAN consensus (cross-datacenter Raft)
- Byzantine fault tolerance at practical scale without cryptographic overhead
- Reconfiguration — safely changing cluster membership while live
- Leaderless consensus with acceptable tail latency

## My position

Raft has won practical adoption because of its understandability — a lesson that algorithm design for systems requires communication, not just correctness. Paxos remains theoretically important but is notoriously hard to implement correctly.

## Research gaps

- Few systematic studies comparing consensus implementations under realistic failure injection
- Limited work on consensus in heterogeneous (cloud + edge) topologies
- Interaction between consensus and modern hardware (RDMA, NVM) is underexplored

## Key people
