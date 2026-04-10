Chapter 14. Observability and
the Software Supply Chain

This chapter is contributed by Frank Chen, senior staﬀ
software engineer at Slack

A NOTE FROM CHARITY, LIZ, AND GEORGE
So far in this book, we’ve examined observability as it
relates to the code you write and how that code operates in
production. But running in production is only one stage in
your code’s life cycle. Prior to running in production,
automatically testing and deploying your code with build
pipelines is common practice. Delving into speciﬁc
continuous integration (CI) / continuous deployment (CD)
architectures and practices is beyond the scope of this book,
except for how observability can be used to debug pipeline
issues.

Production is not the only ever-changing environment your
code encounters. The systems you use to run your build
pipelines can also change in unexpected and often
unpredictable ways. Like applications we’ve discussed in
this book, build system architectures can vary widely—from
monolithic single nodes to vast build farms running parallel
processes at scale. Systems with simpler architectures may
be easier to debug by reasoning your way through potential
failures. But once a system reaches a certain degree of
complexity, observability can be an indispensable—and
sometimes required—debugging tool to understand what’s
happening in your CI/CD pipelines. Just as in production,
issues such as poor integration, invisible bottlenecks, and an
inability to detect issues or debug their causes can also
plague your build systems.

This chapter, written by Frank Chen, details how Slack uses
observability to manage its software supply chain. We are so
pleased to include Chen’s work in this book, because it’s a
great example of using observability to build systems
running at scale. You’ll learn about how and where to use
traces and observability to debug issues in your build

pipelines, and the types of instrumentation that are
particularly useful in this context.

Slack’s story is framed from the point of view of an
organization with large-scale software supply chains,
though we believe it has lessons applicable at any scale. In
Part IV, we’ll speciﬁcally look at challenges that present
themselves when implementing observability at scale.

I’m delighted to share this chapter on practices and use cases
for integrating observability into your software supply chain. A
software supply chain comprises “anything that goes into or
aﬀects your software from development, through your CI/CD
pipeline, until it gets deployed into production.”

1

For the past three years, I have spent time building and
learning about systems and human processes to deliver
frequent, reliable, and high-quality releases that provide a
simpler, more pleasant, and productive experience for Slack
customers. For teams working on the software supply chain, the
pipelines and tools to support CI/CD used by our wider
organization are our production workload.

Slack invested early in CI development for collaboration and in
CD for releasing software into the hands of customers. CI is a
development methodology that requires engineers to build, test,
and integrate new code as frequently as possible to a shared
codebase. Integration and veriﬁcation of new code in a shared
codebase increases conﬁdence that new code does not
introduce expected faults to customers. Systems for CI enable
developers to automatically trigger builds, test, and receive
feedback when they commit new code.

NOTE

For a deeper dive into continuous integration, see “Continuous
Architecture and Continuous Delivery” by Murat Erder and Pierre Pureur
on the ScienceDirect website. In addition, “How to Get Started with
Continuous Integration” by Sten Pittet on the Atlassian website is a
particularly good guide.

Slack evolved from a single web app PHP monorepo (now
mostly in Hack) to a topology of many languages, services, and
clients to serve various needs. Slack’s core business logic still
lives in the web app and routes to downstream services like
Flannel. CI workﬂows at Slack include unit tests, integration
tests, and end-to-end functional tests for a variety of codebases.

For the purposes of this chapter, I focus on observability into
our CI/CD systems and web app’s CI, as this is where many
engineers at Slack spend the majority of their time. The web
app CI ecosystem spans Checkpoint, Jenkins builder/test
executors, and QA environments (each capable of running
Slack’s web app codebase that routes to supporting dependent
services). Checkpoint is an internally developed service that
orchestrates CI/CD workﬂows. It provides an API and frontend
for orchestrating stages of complex workﬂows like test
execution and deployments. It also shares updates in Slack to
users for events like test failures and pull request (PR) reviews.

Figure 14-1 shows an example workﬂow of an end-to-end web
app test. A user pushes a commit to GitHub, Checkpoint
receives webhooks from GitHub for codebase-related events,
like a new commit. Checkpoint then sends requests to Jenkins
for build and test workﬂows to be performed by Jenkins
executors. Inside Jenkins builder and test executors, we use a
codebase called CIBot that executes build and test scripts with a
merge against the main branch (and then communicates with
Checkpoint for orchestration and test result posting).

Figure 14-1. An example end-to-end workﬂow for testing the web app

Why Slack Needed Observability
Throughout its life cycle, Slack has grown tremendously in both
customer count and codebases. While this is exciting for us,
growth has a shadow side that can lead to increased complexity,
fuzzy boundaries, and systems stretched to their limits. Test
suite executions that were once measured in low thousands per
day grew to high hundreds of thousands. Those workloads have
a changing, diverse nature across codebases and many teams.

At that scale, it’s necessary to control costs and compute
resources with strategies like adaptive capacity and
oversubscription.

NOTE

More details about Slack’s CI systems and cost-control strategies can be
found in Slack Engineering’s blog article “Infrastructure Observability for
Changing the Spend Curve”.

As a result, our workﬂows to test and deploy code in a
development environment could often have more complexity
than some production services. Underlying dependencies in
infrastructure types or runtime versions could unexpectedly
change and introduce unintended failures. For example, Slack
relies on Git for version control. Diﬀerent versions of Git can
have radically diﬀerent performance characteristics when
merging code. Anomaly detection on CI surfaces can involve
debugging issues that might be in your code, test logic,
dependent services, underlying infrastructure, or any
permutation therein. When something goes wrong, issues could
be hidden in any number of unpredictable places. Slack quickly
realized we needed observability in our software supply chain.

Instrumenting the software supply chain is a competitive
advantage, both for Slack and for your own business. Faster
development + faster release cycles = better service for your
customers. Observability played a large role in Slack’s
understanding of problems and in framing investments in
CI/CD. In the following sections, you’ll read about Slack
instrumenting Checkpoint with improved distributed traces in
2019, and then case studies from 2020 and 2021 for speciﬁc
problem solutions.

Internal tooling typically goes through the same multiple
critical systems as production systems except with additional
complexity to execute against development systems, and code
merges for builds and tests. Internal tooling presents a diﬀerent
perspective than production services: the cardinality is
signiﬁcantly lower, but the criticality of any single event and
span are signiﬁcantly higher. A failure at any dependent system
represents a slowdown in developer velocity and frustration by
teams, and ultimately a slowdown to delivering software to
your customers. In other words, if the ﬁrst part of your
software supply chain is slow or failure-prone, the remainder
of your software supply chain—that relies on this critical part—
will be bottlenecked.

“It is slow” is the hardest problem to debug in distributed
systems. “It is ﬂaky” is the most heard problem by teams
supporting internal tools. The common challenge for both is
how to correlate problems in high-complexity systems that
interact. For example, when infrastructure or tests are ﬂaky,
developers experience a decrease in their ability to write code,
and their trust in tooling is eroded, leading to frustration. This
type of complexity led Slack to invest in building shared
observability pipelines. You’ll see more details about
observability pipelines in Chapter 18, written by Slack’s Suman
Karumuri and Ryan Katkov. In the next section, you’ll learn
how dimensionality helps solve this problem.

Instrumentation: Shared Client Libraries
and Dimensions
A primary challenge in Slack’s CI has been complexity. A failure
in an end-to-end test might be the result of multiple interacting
codebases that require views across codebase changes,
infrastructure changes, and platform runtimes. For a single

commit from a web app developer in 2020, our CI pipeline
would execute 30+ test suites that rely on GitHub, build
pipelines by three platform teams (performance, backend, and
frontend), across 20 teams/services with diﬀerent requirements
and areas of expertise. By mid-2020, our CI infrastructure
started to be stretched to its limit, as a 10% month-over-month
growth in test execution led to multiple downstream services
having challenges scaling to meet the additional demand from
test executions.

Slack attempted to solve this series of bottlenecks with
distributed tracing. Slack’s CI infrastructure in 2019 was mostly
written by the CTO and early employees, and it remained
mostly functional for years. But this infrastructure showed
growing pains and lack of observability into many workﬂows.

By applying tracing to a multihop build system, our team was
able to solve multiple challenges in CI workﬂows within hours
of adding instrumentation:

In 2019 Q2, we instrumented our CI runner with an
afternoon prototype. Similarly to other trace use cases,
within minutes of having trace data, we discovered
anomalous runtimes for Git checkout. By looking at the
underlying hosts, we found they were not being updated in
the Auto Scaling group (ASG) like others and were quickly
deprovisioned. This unlocked a simple solution to
workﬂows that were not resulting in errors or failures but
were nonetheless presenting a slow—and therefore bad—
user experience.

In 2019 Q3, our teams were in the midst of a
multiday/multiteam incident. We implemented our ﬁrst
cross-service trace between our CI runner and test
environments, and discovered a Git Large File Storage (LFS)
issue that slowed system throughput. Initially, teams

scrambled to bring multiple overloaded systems under
control as one portion of our system cascaded failures to
other systems. We added simple instrumentation,
borrowed from our CI runner, and were able to resolve the
incident in less than two hours by discovering a set of hosts
that were failing to retrieve artifacts from Git LFS.

In Figure 14-2, you can see a simpliﬁed view of a test run after a
user pushes a commit to GitHub. This test run is orchestrated by
Checkpoint and subsequently passed onto a build step and then
test step, each performed by Jenkins executors. In each stage,
you see additional dimensions that contextualize execution in
CI. Slack engineers then use single, or combinations of,
dimensions as breadcrumbs to explore executions when
performance or reliability issues arise in production. Each
additional dimension is a direction and clue during issue
investigation. You can combine clues to iteratively drill down
for speciﬁc issues in deployed code.

Figure 14-2. A simpliﬁed view of a single end-to-end test run orchestrated by our CI
orchestration layer, highlighting the common dimensions shared across our workﬂow

Client dimensions are conﬁgured within each trace. (Figure 14-3
shows example dimensions.) Slack uses a TraceContext
singleton that sets up these dimensions. Each TraceContext
builds an initial trace with common dimensions and a new
trace. Each trace contains multiple spans and an array of
speciﬁc dimensions at each span. An individual span (e.g., in
Figure 14-4 from runner.test_execution) can contain
context on the original request and add dimensions of interest
to the root span. As you add more dimensions, you add more
context and richness to power issue investigations.

NOTE

You can learn more about wide spans at “CircleCI: The Unreasonable
Eﬀectiveness of a Single Wide Event”, by Glen Mailer, a video posted on
the Honeycomb website.

Figure 14-3. Common dimensions in our Hack codebase. You can use these as examples
for structuring dimensions across spans and services in CI.

For example, Slack engineers might want to identify
concurrency issues along common dimensions (like hostnames
or groups of Jenkins workers). The TraceContext already
provides a hostname tag. The CI runner client then appends a
tag for the Jenkins worker label. Using a combination of these
two dimensions, Slack engineers can then group individual
hosts or groups of Jenkins workers that have runtime issues.

Similarly, Slack engineers might want to identify common build
failures. The CI runner client appends a tag for the commit
head or commit main branch. This combination allows for
identifying which commits a broken build might come from.

The dimensions in Figure 14-3 are then used in various script
and service calls as they communicate with one another to
complete a test run (Figure 14-4).

Figure 14-4. A trace for the CI execution of a backend test suite called backend-php-unit

In the following sections, I’ll share how Slack uses trace tooling
and queries to make sense of the supply chain and how
provenance can result in actionable alerting to resolve issues.

Case Studies: Operationalizing the Supply
Chain
Observability through analyzing telemetry data consisting of
metrics, events, logs, and traces is a key component to modeling
internal customer experiences. The key for Slack infrastructure
tooling and people is to consistently learn and embed
observability into our tooling. This section presents case studies
that bring observability into Slack developers’ workﬂows. I
hope by sharing Slack’s approach to these problems, you can
reuse these patterns for your own internal development.

Understanding Context Through Tooling
CI operates in a complex, distributed system; multiple small
changes can be additive in their eﬀect on the CI user
experience. Multiple teams traditionally operated in silos to
debug performance and resiliency issues in order to better
serve their customers (e.g., backend, frontend, and
middleware). However, for customers of CI who are doing
development and then running tests, the user experience is best
represented by the worst-performing or ﬂakiest tests. A test is
considered ﬂaky when running the same code has a diﬀerent
result. Understanding context is critical for identifying
bottlenecks.

For the rest of this section, I will walk through a case study of
Slack teams working together to understand context from the
problem of ﬂaky tests. Slack teams were able to signiﬁcantly

reduce this problem for their internal customers by focusing on
a few key tenets:

Instrumenting the test platform with traces to capture
previously underexplored runtime variables

Shipping small, observability-driven feedback loops to
explore interesting dimensionality

Running reversible experiments on dimensions that
correlated with ﬂaky test conﬁgurations

Developer frustration across Slack engineering was increasing
because of ﬂaky end-to-end test runs in 2020. Test turnaround
time (p95) was consistently above 30 minutes for a single
commit (the time between an engineer pushing a commit to
GitHub and all test executions returning). During this period,
most of Slack’s code testing was driven by end-to-end tests
before an engineer merged their code to the mainline. Many
end-to-end test suites had an average suite execution ﬂake rate
of nearly 15%. Cumulatively, these ﬂaky test executions peaked
at 100,000 weekly hours of compute time on discarded test
executions.

By mid-2020, the combination of these metrics led to
automation teams across Slack sharing a daily 30-minute triage
session to dig into speciﬁc test issues. Automation team leads
hesitated to introduce any additional variance to the way Slack
used Cypress, an end-to-end testing platform. The belief was
that ﬂakiness was from the test code itself. Yet no great progress
was made in verifying or ruling out that belief.

In late 2020, observability through tracing had shown great
promise and impact in identifying infrastructure bottlenecks in
other internal tooling. Internal tooling and automation teams
worked to add tracing for a few runtime parameters and spans
in Cypress.

Within days of instrumentation, multiple dimensions appeared
very correlated with test suites that had higher ﬂake rates.
Engineers from these teams looked at this instrumentation and
discovered that users and test suite owners of the test platform
had drastically diﬀerent conﬁgurations. During this discovery
process, additional telemetry was added to the Docker runtime
to add additional color to some ﬂakes. Empowered with data,
these engineers experimented to place better defaults for the
platform and to place guardrails for ﬂaky conﬁgurations. After
these initial adjustments, test suite ﬂake rates decreased
signiﬁcantly for many users (suites went from 15% to under
0.5% ﬂake rates), as shown in Figure 14-5.

Because of the disparate nature of the runtime between end-to-
end test suites that no central team had visibility into, context
gathering became a critical piece between suites to identify
speciﬁc dimensions that caused ﬂakiness.

NOTE

For more on how Slack evolved its testing strategy and culture of safety,
see the Slack blog post “Balancing Safety and Velocity in CI/CD at Slack”.
Slack describes how engineers initiated a project to transform testing
pipelines and de-emphasize end-to-end testing for code safety. This
drastically reduced user-facing ﬂakiness and increased developer velocity
in 2021.

Figure 14-5. Time spent on ﬂaking test runs between major classes of test runs for web
app. The light colored bar shows ﬂaky test executions from the Cypress platform tests.

With this shared understanding of context through tooling,
Slack’s next step was to embed actionable workﬂows through
alerting.

Embedding Actionable Alerting
Slack integrates its own product into how engineers handle
their development and triage issues in the infrastructure.
Observability through tracing plays a critical role in helping
engineers do their job by directing people in Slack messages
and conﬁgured dashboards.

Let’s examine a case study around test execution. A single test
suite execution might be understood in diﬀerent ways
depending on code, infrastructure, or features in the product.
Each team or platform might have multiple SLOs for various
parts of a test execution. Here are a few examples:

Test suite owner or platform teams might care about
ﬂakiness, reliability, or memory usage.

Test infrastructure teams might care about performance
and reliability of speciﬁc operations (like Docker ops or cost
per test).

Deployment owners might care about what was tested or
upcoming hotﬁxes coming through CI.

Internal tooling teams might care about throughput of test
result processing through CI.

The prompt for identifying an issue might be anomaly detection
alerts for a high-level business metric or a speciﬁc issue that’s
suite based (e.g., in Figure 14-6). The link to our observability
tool might direct the user to a collection of views available
based on the test_suite dimension.

Figure 14-6. Identifying runtime increase for test suite above p50

At Slack, we’ve encouraged teams to make dashboards based on
speciﬁc use cases. The Honeycomb link brings up a query from
our CI Service Traces dashboard (Figure 14-7) that has
parameters set for a potential issue for a test suite. This
message helps inform responders of a speciﬁc issue—for
example, a test suite called backend-php-integration is showing
signs of a longer runtime—and responders might use
Honeycomb to look at associated traces for potential issues.

Figure 14-7. Slack’s CI Service Traces dashboard displaying queries available to view
diﬀerent pieces of CI interactions

In Figure 14-8, you can see an example of a query looking at a
high level at a rate, error, and duration query that responding
teams might use.

Figure 14-8. This sample drill-down query approximates a rate, error, and duration
(RED) dashboard with visualizations by grouping individual methods between services
in Checkpoint

With actionable alerting embedded, now we can understand
what changed.

Understanding What Changed
Let’s explore another case study of an August 2021 incident that
combines a few of the preceding ideas. At Slack, we use the
incident command system to handle incidents when an outage
or service degradation is detected. The incident response begins
with a new public Slack channel, and an incident commander
adds responders from multiple teams to coordinate response
and remediation of an outage.

In this situation, multiple users noted being blocked after seeing
high rates of failures due to out-of-memory errors (OOMs) on
test suite execution for backend unit and integration test suites.
Each of these backend unit test suites may run tens of
thousands of tests, and individually, test suite executions were
occasionally passing.

Early in the incident, a responder found an anomaly from the
previous day noting a higher ﬂake rate (see Figure 14-9 for
types of anomalies), potentially pointing to something that
changed around that time. During the incident, responders
looked at test case traces from backend tests to look at jumps in
memory footprint for test cases. We were able to see multiple
jumps in memory usage at p50, p95, and p99 over the last
months, with ﬁdelity down to the hour on what had changed.

Using this data, experts were able to identify potential PRs from
the previous day and more from the previous months that
appeared correlated with jumps in memory usage. Causation
for degradations in large codebases or test suites are often
challenging because of a high velocity of change and many
variables both in the codebase and infrastructure that might
lead to changes.

Figure 14-9. The Conditions section of a Conditions/Actions/Needs (CAN) process from
that incident. There is a symptom of the outage that multiple test suites are failing due
to OOM, and an ongoing theory that’s being investigated.

A few potential culprit commits were reverted. Because of the
potential large number of variables during an incident
investigation, a holding pattern frequently occurs after a
change, before telemetry can report healthiness. Figure 14-10
shows a long thread by subject-matter experts who were
quickly able to test the hypothesis and see system health using
distributed tracing in near-real time.

Figure 14-10. A Slack thread of questions during incident investigation that starts with
testing a hypothesis, taking action, and using observability to validate the hypothesis
(responder names blurred for privacy)

This data allowed Slack to look at telemetry with context over
time. This is one of many examples of using observability in
day-to-day operations at Slack. You can adopt a similar
approach to identify changes and breaks by embedding
observability into your own investigations.

Conclusion
This chapter illustrates how observability can be useful in the
software supply chain. I shared how Slack instrumented the CI
pipeline and recent examples of debugging distributed systems.
The intricacies of debugging distributed systems are generally
top of mind for application developers trying to understand
how their code behaves in production environments. But, prior
to production, other distributed systems may be equally
challenging to properly understand and debug.

With the right tools and dimensionality in the software supply
chain, Slack engineers were able to solve complex problems
throughout the CI workﬂow that were previously invisible or
undetected. Whether debugging complaints that an application
is slow or that CI tests are ﬂaky, observability can help
developers correlate problems in high-complexity systems that
interact.

1  Maya Kaczorowski, “Secure at Every Step: What is Software Supply Chain

Security and Why Does It Matter?”, GitHub Blog, September 2, 2020.

Part IV. Observability at Scale

In Part III, we focused on overcoming barriers to getting started
and new workﬂows that help change social and cultural
practices in order to put some momentum behind your
observability adoption initiatives. In this part, we examine
considerations on the other end of the adoption spectrum: what
happens when observability adoption is successful and
practiced at scale?

When it comes to observability, “at scale” is probably larger
than most people think. As a rough ballpark measure, when
measuring telemetry events generated per day in the high
hundreds of millions or low billions, you might have a scale
issue. The concepts explored in this chapter are most acutely
felt when operating observability solutions at scale. However,
these lessons are generally useful to anyone going down the
path of observability.

Chapter 15 explores the decision of whether to buy or build an
observability solution. At a large enough scale, as the bill for
commercial solutions grows, teams will start to consider
whether they can save more by simply building an
observability solution themselves. This chapter provides
guidance on how best to approach that decision.

Chapter 16 explores how a data store must be conﬁgured in
order to serve the needs of an observability workload. To
achieve the functional requirements of iterative and open-
ended investigations, several technical criteria must be met.
This chapter presents a case study of Honeycomb’s Retriever
engine as a model for meeting these requirements.

Chapter 17 looks at how to reduce the overhead of managing
large volumes of telemetry data at scale. This chapter presents
several techniques to ensure high-ﬁdelity observability data,
while reducing the overall number of events that must be
captured and stored in your backend data store.

Chapter 18 takes a look at another technique for managing
large volumes of telemetry data at scale, or management via
pipelines. This is a guest chapter by Suman Karumuri, senior
staﬀ software engineer, and Ryan Katkov, director of
engineering, at Slack. It presents an in-depth look at how Slack
uses telemetry management pipelines to route observability
data at scale.

This part of the book focuses on observability concepts that are
useful to understand at any scale but that become critical in
large-scale use cases. In Part V, we’ll look at techniques for
spreading observability culture at any scale.


