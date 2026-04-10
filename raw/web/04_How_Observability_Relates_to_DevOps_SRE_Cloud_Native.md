Chapter 4. How Observability
Relates to DevOps, SRE, and
Cloud Native

So far, we’ve referenced observability in the context of modern
software systems. Therefore, it’s important to unpack how
observability ﬁts into the landscape of other modern practices
such as the DevOps, site reliability engineering (SRE), and cloud
native movements. This chapter examines how these
movements have both magniﬁed the need for observability and
integrated it into their practices.

Observability does not exist in a vacuum; instead, it is both a
consequence and an integral part of the DevOps, SRE, and cloud
native movements. Like testability, observability is a property
of these systems that improves understanding of them.
Observability and testability require continuous investment
rather than being a one-time addition, or having a one-size-ﬁts-
all solution. As they improve, beneﬁts accrue for you, as a
developer, and for end users of your systems. By examining
why these movements created a need for observability and
integrated its use, you can better understand why observability
has become a mainstream topic and why increasingly diverse
teams are adopting this practice.

Cloud Native, DevOps, and SRE in a
Nutshell
In contrast with the monolithic and waterfall development
approaches that software delivery teams employed in the 1990s

to early 2000s, modern software development and operations
teams increasingly use cloud native and Agile methodologies. In
particular, these methodologies enable teams to autonomously
release features without tightly coupling their impact to other
teams. Loose coupling unlocks several key business beneﬁts,
including higher productivity and better proﬁtability. For
example, the ability to resize individual service components
upon demand and pool resources across a large number of
virtual and physical servers means the business beneﬁts from
better cost controls and scalability.

NOTE

For more examples of the beneﬁts of Agile and cloud native
methodologies, see the DevOps Research and Assessment (DORA) 2019
Accelerate State of DevOps Report by Nicole Forsgren et al.

However, cloud native has signiﬁcant trade-oﬀs in complexity.
An often overlooked aspect of introducing these capabilities is
the management cost. Abstracted systems with dynamic
controls introduce new challenges of emergent complexity and
nonhierarchical communications patterns. Older monolithic
systems had less emergent complexity, and thus simpler
monitoring approaches suﬃced; you could easily reason about
what was happening inside those systems and where unseen
problems might be occurring. Today, running cloud native
systems feasibly at scale demands more advanced
sociotechnical practices like continuous delivery and
observability.

The Cloud Native Computing Foundation (CNCF) deﬁnes cloud
native as “building and running scalable applications in
modern, dynamic environments...[Cloud native] techniques
enable loosely coupled systems that are resilient, manageable,

and observable. Combined with robust automation, they allow
engineers to make high-impact changes frequently and
predictably with minimal toil.” By minimizing toil (repetitive
manual human work) and emphasizing observability, cloud
native systems empower developers to be creative. This
deﬁnition focuses not just on scalability, but also on
development velocity and operability as goals.

NOTE

For a further look at what it means to eliminate toil, we recommend
Chapter 5 of Site Reliability Engineering, edited by Betsy Beyer et al.
(O’Reilly).

The shift to cloud native doesn’t only require adopting a
complete set of new technologies, but also changing how people
work. That shift is inherently sociotechnical. On the surface,
using the microservices toolchain itself has no explicit
requirement to adopt new social practices. But to achieve the
promised beneﬁts of the technology, changing the work habits
also becomes necessary. Although this should be evident from
the stated deﬁnition and goals, teams typically get several steps
in before realizing that their old work habits do not help them
address the management costs introduced by this new
technology. That is why successful adoption of cloud native
design patterns is inexorably tied to the need for observable
systems and for DevOps and SRE practices.

Similarly, DevOps and SRE both highlight a desire to shorten
feedback loops and reduce operational toil in their deﬁnitions
and practices. DevOps provides “Better Value, Sooner, Safer, and
Happier”  through culture and collaboration between
development and operations groups. SRE joins together systems
engineering and software skill sets to solve complex operational

1

problems through developing software systems rather than
manual toil. As we’ll explore in this chapter, the combination of
cloud native technology, DevOps and SRE methodologies, and
observability are stronger together than each of their
individual parts.

Observability: Debugging Then Versus Now
The goal of observability is to provide a level of introspection
that helps people reason about the internal state of their
systems and applications. That state can be achieved in various
ways. For example, you could employ a combination of logs,
metrics, and traces as debugging signals. But the goal of
observability itself is agnostic in terms of how it’s accomplished.

In monolithic systems, you could anticipate the potential areas
of failure and therefore could debug your systems by yourself
and achieve appropriate observability by using verbose
application logging, or coarse system-level metrics such as
CPU/disk utilization combined with ﬂashes of insight. However,
these legacy tools and instinctual techniques no longer work for
the new set of management challenges created by the
opportunities of cloud native systems.

Among the example technologies that the cloud native
deﬁnition mentions are containers, service meshes,
microservices, and immutable infrastructure. Compared to
legacy technologies like virtual machines and monolithic
architectures, containerized microservices inherently introduce
new problems such as cognitive complexity from
interdependencies between components, transient state
discarded after container restart, and incompatible versioning
between separately released components. Immutable
infrastructure means that it’s no longer feasible to ssh into a
host for debugging, as it may perturb the state on that host.

Service meshes add an additional routing layer that provides a
powerful way to collect information about how service calls are
happening, but that data is of limited use unless you can
analyze it later.

Debugging anomalous issues requires a new set of capabilities
to help engineers detect and understand problems from within
their systems. Tools such as distributed tracing can help capture
the state of system internals when speciﬁc events occurred. By
adding context in the form of many key-value pairs to each
event, you will create a wide, rich view of what is happening in
all the parts of your system that are typically hidden and
impossible to reason about.

For example, in a distributed, cloud native system, you may ﬁnd
it diﬃcult to debug an issue occurring across multiple hosts by
using logs or other noncorrelated signals. But by utilizing a
combination of signals, you could systematically drill down into
anomalous behavior starting from the high level of your service
metrics, iterating until you discover which hosts are most
relevant. Sharding logs by host means you no longer need
centralized retention and indexing of all logs as you would for a
monolith. To understand the relationships among
subcomponents and services in a monolith or distributed
system, you previously may have needed to keep the
relationships of all system components in your head.

Instead, if you can use distributed tracing to break down and
visualize each individual step, you need to understand the
complexity of your dependencies only as they impact execution
of a speciﬁc request. Understanding which calling and receiving
code paths are associated with which versions of each service
allows you to ﬁnd reverse compatibility problems and any
changes that broke compatibility.

Observability provides a shared context that enables teams to
debug problems in a cohesive and rational way, regardless of a
system’s complexity, rather than requiring one person’s mind to
retain the entire state of the system.

Observability Empowers DevOps and SRE
Practices
It’s the job of DevOps and SRE teams to understand production
systems and tame complexity. So it’s natural for them to care
about the observability of the systems they build and run. SRE
focuses on managing services according to service level
objectives (SLOs) and error budgets (see Chapters 12 and 13).
DevOps focuses on managing services through cross-functional
practices, with developers maintaining responsibility for their
code in production. Rather than starting with a plethora of
alerts that enumerate potential causes of outages, mature
DevOps and SRE teams both measure any visible symptoms of
user pain and then drill down into understanding the outage by
using observability tooling.

The shift away from cause-based monitoring and toward
symptom-based monitoring means that you need the ability to
explain the failures you see in practice, instead of the
traditional approach of enumerating a growing list of known
failure modes. Rather than burning a majority of their time
responding to a slew of false alarms that have no bearing on the
end-user visible performance, teams can focus on
systematically winnowing hypotheses and devising mitigations
for actual system failures. We cover this in greater detail in
Chapter 12.

Beyond the adoption of observability for break/ﬁx use cases,
forward-thinking DevOps and SRE teams use engineering
techniques such as feature ﬂagging, continuous veriﬁcation,

and incident analysis. Observability supercharges these use
cases by providing the data required to eﬀectively practice
them. Let’s explore how observability empowers each:

Chaos engineering and continuous veriﬁcation

These require you to have observability to “detect when the

system is normal and how it deviates from that steady-state

as the experiment’s method is executed.”  You cannot

2

meaningfully perform chaos experiments without the ability

to understand the system’s baseline state, to predict

expected behavior under test, and to explain deviations

from expected behavior. “There is no point in doing chaos

engineering when you actually don’t know how your system

is behaving at your current state before you inject chaos.”

3

Feature ﬂagging

This introduces novel combinations of ﬂag states in

production that you cannot test exhaustively in

preproduction environments. Therefore, you need

observability to understand the individual and collective

impact of each feature ﬂag, user by user. The notion of

monitoring behavior component by component no longer

holds when an endpoint can execute in multiple ways

depending on which user is calling it and which feature ﬂags

are enabled.

Progressive release patterns

These patterns, such as canarying and blue/green

deployment, require observability to eﬀectively know when

to stop the release and to analyze whether the system’s

deviations from the expected are a result of the release.

Incident analysis and blameless postmortem

These require you to construct clear models about your

sociotechnical systems—not just what was happening inside

the technical system at fault, but also what the human

operators believed was happening during the incident. Thus,

robust observability tooling facilitates performing excellent

retrospectives by providing an ex post facto paper trail and

details to cue retrospective writers.

Conclusion
As the practices of DevOps and SRE continue to evolve, and as
platform engineering grows as an umbrella discipline, more
innovative engineering practices will inevitably emerge in your
toolchains. But all of those innovations will depend upon
having observability as a core sense to understand your
modern complex systems. The shift toward DevOps, SRE, and
cloud native practices have created a need for a solution like
observability. In turn, observability has also supercharged the
capabilities of teams that have adopted its practice.

1  Jonathan Smart, “Want to Do an Agile Transformation? Don’t. Focus on Flow,

Quality, Happiness, Safety, and Value”, July 21, 2018.

2  Russ Miles, Chaos Engineering Observability (Sebastopol, CA: O’Reilly, 2019).

3  Ana Medina, “Chaos Engineering with Ana Medina of Gremlin”, o11ycast

podcast, August 15, 2019.

Part II. Fundamentals of
Observability

In the ﬁrst part of this book, we examined the deﬁnition of
“observability,” its necessity in modern systems, its evolution
from traditional practices, and the way it is currently being
used in practice. This second section delves deeper into
technical aspects and details why particular requirements are
necessary in observable systems.

Chapter 5 introduces the basic data type necessary to build an
observable system—the arbitrarily wide structured event. It is
this fundamental data type for telemetry that makes the
analysis described later in this part possible.

Chapter 6 introduces distributed tracing concepts. It breaks
down how tracing systems work in order to illustrate that trace
data is simply a series of interrelated arbitrarily wide
structured events. This chapter walks you through manually
creating a minimal trace with code examples.

Chapter 7 introduces the OpenTelemetry project. While the
manual code examples in Chapter 6 help illustrate the concept,
you would more than likely start with an instrumentation
library. Rather than choosing a proprietary library or agent that
locks you into one vendor’s particular solution, we recommend
starting with an open source and vendor-neutral
instrumentation framework that allows you to easily switch
between observability tools of your choice.

Chapter 8 introduces the core analysis loop. Generating and
collecting telemetry data is only a ﬁrst step. Analyzing that data
is what helps you achieve observability. This chapter introduces
the workﬂow required to sift through your telemetry data in
order to surface relevant patterns and quickly locate the source
of issues. It also covers approaches for automating the core
analysis loop.

Chapter 9 reintroduces the role of metrics as a data type, and
where and when to best use metrics-based traditional
monitoring approaches. This chapter also shows how
traditional monitoring practices can coexist with observability
practices.

This part focuses on technical requirements in relation to the
workﬂow necessary to shift toward observability-based
debugging practices. In Part III, we’ll examine how those
individual practices impact team dynamics and how to tackle
adoption challenges.


