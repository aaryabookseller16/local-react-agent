# Local ReAct Agent Project Roadmap

Source of truth for scope and sequence. When my memory or a chat conflicts with this file, this file wins. Update it when a decision changes.

Size tags: **S** = one session, **M** = a few sessions, **L** = a week+ of hour-a-day work.

No calendar dates by design (slippage rule: cut scope, don’t extend deadlines).

---

# What this project is

A local ReAct agent built from scratch — no LangChain/LlamaIndex — running on Ollama with an 8B model (Llama 3.1 8B). The point is to build the primitives by hand so I understand what frameworks hide. A separate weekend later ports a slice to LangChain; that port is only meaningful *because* the scratch build came first.

The first six phases form the MVP. Anything after Phase 6 is optional specialization.

This project has two equally important purposes:

1. **AI engineering:** understand how agents actually work and become fluent in building and orchestrating them.
2. **CS and systems foundations:** rebuild the computer science foundations that matter for practical software, infrastructure, and AI engineering by learning them alongside a real system.

The project is therefore both a portfolio project and a structured way to learn:

- Software design
- Linux
- Operating systems
- Databases
- Information retrieval
- Networking
- Security
- Containers
- Testing
- Observability
- Concurrency
- Computer systems
- Distributed-systems fundamentals
- Deployment

The distinction throughout the roadmap is:

> **Learn foundational CS concepts deeply. Learn individual technologies just-in-time.**
> 

Linux processes matter beyond this project. Docker commands do not.

Networking fundamentals matter beyond this project. FastAPI syntax does not.

Database concepts matter beyond this project. pgvector-specific syntax does not.

The project provides the practical system against which the foundational concepts can be understood.

Data structures and algorithms are deliberately excluded as a learning objective because they are covered separately through LeetCode.

---

# Learning model

Each phase has two parallel lanes:

```
PROJECT                         FOUNDATION

Build something useful    ↔    Understand what makes it work
```

Neither replaces the other.

Reading never gates building, but implementation alone is also insufficient for foundational topics.

For foundational concepts:

```
learn concept
→ experiment with concept
→ use concept in project
→ explain why it works
```

For technologies:

```
learn enough
→ use it
→ consult documentation as needed
```

## Foundation map

```
PROJECT                         CS / ENGINEERING FOUNDATION

Phase 0 — Core agent        ↔   Programming
                                Abstraction
                                Parsing
                                Software architecture

Phase 1 — File tools        ↔   Linux
                                Filesystems
                                Permissions
                                OS interfaces

Phase 2 — Memory            ↔   Databases
                                SQL
                                Data modeling
                                Information retrieval

Phase 3 — Planning          ↔   State machines
                                Control flow
                                Software architecture
                                Reliability

Phase 4 — Sandbox           ↔   Operating systems
                                Processes
                                Networking
                                Security
                                Containers
                                Resource isolation

Phase 5 — Evaluation        ↔   Software testing
                                Observability
                                Experimental design
                                Reliability engineering

Phase 6 — Orchestration     ↔   Concurrency
                                Operating systems
                                Resource management
                                Computer systems
                                Distributed-systems fundamentals
```

After the MVP:

```
OPTIONAL PROJECT WORK            DEEPER FOUNDATION

LangChain / LangGraph        ↔   Framework design / abstraction

Langfuse                     ↔   Observability / production AI

Remote control               ↔   Networking / backend systems

Container internals          ↔   Operating systems / Linux

Kubernetes                   ↔   Distributed systems / orchestration

Cloud deployment             ↔   Networking / infrastructure

CI/CD                        ↔   Software delivery / automation

Multi-agent systems          ↔   Coordination / distributed systems

Model serving / MLOps        ↔   Systems performance / GPU resources
```

---

# Industry-currency lane — parallel, time-boxed

## Why

The scratch-first sequence is deliberate: primitives before frameworks. But strictly gating all framework/API exposure until after the Phase 6 MVP risks reaching month 3 without ever touching what AI-engineering job postings actually name — hosted tool-calling APIs, LangChain/LangGraph, vector DB services, eval tooling. This lane closes that gap without displacing the scratch build or changing phase scope.

## Rules

- Capped at ~1–2 hours/week, tracked separately from phase time budgets. It never extends a phase deadline — the slippage rule still applies to the main lane only.
- Reading and comparing, not building. No parallel project, no framework code merged into this repo. A five-line standalone script in a scratch folder is fine; a second agent implementation is not.
- Each item is anchored to a phase that's already in progress or done, so the comparison is meaningful — you need your own primitive before a framework's version of it means anything.
- This lane is the first thing the anti-displacement flag cuts if a week is tight. The scratch build is never cut for it.

## Phase → industry-currency mapping

Do the mapped item any time after that phase's own exit condition is met — not before.

| Phase | Time-boxed industry action (~30–60 min) |
| --- | --- |
| Phase 0 — Core agent | Read OpenAI's and Anthropic's tool-calling/function-calling docs. Compare their JSON schema for a tool call against your own `Action:`/`Action Input:` format. |
| Phase 1 — File tools | Superseded — Phase 1 now builds `list_directory`/`search_files`/`summarize_pdf` as real MCP tools (see Phase 1 Build above) instead of just reading the spec. |
| Phase 2 — Memory | Read one hosted vector DB's docs (Pinecone or Weaviate) for 30 min. Note what pgvector does by hand that the hosted service abstracts away. |
| Phase 3 — Planning | Read LangGraph's "Thinking in LangGraph" doc. Map your ad-hoc multi-step flow onto its state-graph model. |
| Phase 4 — Sandbox | Skim how a hosted agent-sandbox product documents its isolation guarantees. Compare to what Docker gives you by hand. |
| Phase 5 — Evaluation | Skim one LLM eval framework (promptfoo or Ragas) for how it structures test cases vs. your harness. |
| Phase 6 — Orchestration | Read how one production agent framework (LangGraph, CrewAI, or AutoGen) describes multi-agent fan-out. |

## Optional Phase A trigger — loosened

Previously: only after the full MVP. Now: Optional Phase A (the LangChain/LangGraph port) may start in parallel once Phase 3 is done — by then the ReAct loop, tool registry, and multi-step control flow already exist, which is enough for the scratch-vs-framework comparison to be meaningful. It still runs in parallel, time-boxed under this lane's rules, and never displaces Phases 4–6.

---

# Stack

Verify versions against current docs — this area moves fast.

## MVP

- Python
- Ollama
- Llama 3.1 8B
- Temperature 0 for format reliability
- Hand-written parser + ReAct loop
- PostgreSQL
- pgvector
- nomic-embed-text embeddings
- Docker
- asyncio
- OpenTelemetry

## Optional later

- LangChain
- LangGraph
- Langfuse
- FastAPI
- SSH
- Tailscale or equivalent private networking
- Docker Compose
- Cloud VM
- GitHub Actions
- Kubernetes

## Phase 0 — Core agent — DONE ✅

## Subtask: Chat loop & stateful messages ✅

A chat loop — the base program shape everything else runs inside. Keeps a stateful `messages` list so the model sees the full conversation, including tool results, on every call.

**Learn** (~1 day)
- Program state, control flow, functions, interfaces, separation of concerns

**Resources**
- [Python Tutorial](https://docs.python.org/3/tutorial/) — Data structures, Functions, Modules, Exceptions
- [Pro Git](https://git-scm.com/book/en/v2) — Chapters 1–3, for the commit-often habit this whole project runs on

**Implement**
- [x] Stateful `messages` list
- [x] Basic request/response loop against Ollama

## Subtask: ReAct prompt + hand-written parser ✅

The ReAct format prompt and its parser. Turns the model's free-text reply into a structured `(thought, action, action_input)` the surrounding program can act on, instead of trusting the model to emit valid code.

**Learn** (~1–2 days)
- Parsing: raw text → syntax → parser → structured representation → validation → execution
- Why syntax needs a grammar, valid vs. invalid input, parsing vs. execution, error recovery

**Resources**
- [ReAct paper](https://arxiv.org/abs/2210.03629) — the reasoning/action/observation loop this format implements

**Implement**
- [x] ReAct-format system prompt (Thought/Action/Action Input / Thought/Final Answer)
- [x] Hand-written parser (`parse_input`) producing a structured tuple

## Subtask: Tool registry + calculator ✅

A dict-based tool registry and a real calculator tool. This is the concrete proof that the model proposes an action but never executes it — the surrounding software does, through a lookup and a dispatch call.

**Learn** (~1 day)
- Dispatch, validation, exceptions
- AI systems: LLM → proposed action → deterministic program → tool → observation → LLM

**Resources**
- (project-internal — direct application of the parsing/dispatch concepts above, no separate external resource)

**Implement**
- [x] Dict-based tool registry
- [x] Calculator tool (`ast`-based safe eval, not `eval`)

## Subtask: Robustness & retry handling ✅

Failure handling around the loop: bad tool names, missing input, and off-format replies get a targeted correction fed back to the model instead of crashing, with a capped retry count and a clean give-up.

**Learn** (~1 day)
- Failure handling, error recovery, exceptions

**Resources**
- (project-internal — same parsing/validation material as the parser subtask, applied to failure paths)

**Implement**
- [x] Detect bad tool name vs. missing input vs. off-format reply, and correct each differently
- [x] Capped retries (3)
- [x] Clean give-up after retries exhausted

---

## Tech stack learned

- Python
- Ollama
- Llama 3.1
- Python `ast`
- Git

## Prerequisites

- Basic Python
- Functions
- Lists
- Dictionaries
- Loops
- Exceptions
- Terminal basics

## Exit condition

Already satisfied.

A local model can receive a task, choose the calculator, execute it through the registry, observe the result, and return an answer while failing cleanly on malformed responses.

---

# Phase 1 — More tools — M 🔵

**MCP decision:** `list_directory`/`search_files`/`summarize_pdf` are built as MCP tools inside a small server using the official Python MCP SDK's `FastMCP` high-level API (decorator-based, similar feel to FastAPI). `chat.py` and its existing dict-based dispatch stay exactly as they are — `read_file`/`calculator` are not migrated. Wiring an MCP *client* into `chat.py` so the loop can actually call these tools is a separate, later decision — not bundled into this one.

## Subtask: `read_file` ✅

`read_file` — a tool (plain function, `chat.py`'s dict dispatch). Lets the agent read the contents of a file inside the project directory, so it can answer questions about local files or feed their content into further reasoning.

**Learn** (~1 day)
- Linux filesystem hierarchy, absolute vs. relative paths, home directory
- Permissions: user/group/others, read/write/execute
- Path traversal, allow-listing, why model-generated paths are untrusted

**Resources**
- [Linux Journey](https://linuxjourney.com/) — Command Line, Text-Fu, Permissions
- [Python `pathlib` docs](https://docs.python.org/3/library/pathlib.html)

**Implement**
- [x] Handle bad paths
- [x] Handle missing files
- [x] Handle permission errors
- [x] Path allow-listing (reject traversal outside project dir)
- [x] Safe input handling

## Subtask: `list_directory`

`list_directory` — an MCP tool. Lets the agent enumerate the contents of a directory inside the project, so it can discover what files exist before deciding what to read or search.

**Learn** (~1 day)
- Directories vs. files, metadata (size, mtime), file descriptors conceptually
- MCP tool basics — this is the first MCP tool you're building

**Resources**
- [Python `pathlib` docs](https://docs.python.org/3/library/pathlib.html) — `iterdir`, `stat`
- [MCP Tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [FastMCP quickstart](https://gofastmcp.com/getting-started/quickstart)

**Implement**
- [ ] List entries in an allowed directory only
- [ ] Handle missing/non-directory paths
- [ ] Return structured metadata (name, type, size)
- [ ] Wire as an MCP `@mcp.tool()` function

## Subtask: `search_files`

`search_files` — an MCP tool. Lets the agent find files by name or pattern across the project directory, so it doesn't need to already know a file's exact path.

**Learn** (~1 day)
- Recursive traversal, glob patterns
- `grep`/`find` concepts (for the mental model, not the shell commands themselves)

**Resources**
- [The Linux Command Line](https://linuxcommand.org/tlcl.php) — `grep`, `find` chapters
- [Python `pathlib` docs](https://docs.python.org/3/library/pathlib.html) — `rglob`

**Implement**
- [ ] Recursive search within the allowed directory
- [ ] Pattern/filename matching
- [ ] Shares the same allow-list as `read_file`/`list_directory`
- [ ] Wire as an MCP tool

## Subtask: `summarize_pdf`

`summarize_pdf` — an MCP tool. Extracts text from a PDF and summarizes it through the existing Ollama call, so the agent can digest long documents without dumping raw PDF text into context.

**Learn** (~1–2 days)
- PDF parsing basics, binary file I/O

**Resources**
- [pypdf documentation](https://pypdf.readthedocs.io/en/latest/index.html)

**Implement**
- [ ] Extract text from a PDF
- [ ] Handle corrupt/encrypted PDFs
- [ ] Summarize via the existing Ollama call
- [ ] Wire as an MCP tool

---

## Tech stack learned

- Linux
- Python `pathlib`
- Python file I/O
- PDF parsing (`pypdf`)
- Shell utilities
- MCP (Model Context Protocol) — official Python SDK, `FastMCP`

## Prerequisites

Basic terminal familiarity.

No advanced Linux knowledge required before starting.

## Exit condition

The agent correctly chooses between multiple tools and performs useful read-only operations only inside explicitly allowed directories.

I can explain why the filesystem and permission behavior occurs rather than merely knowing the Python API.

---

# Phase 2 — Memory — L

## Subtask: Persistent conversation history

A relational schema (PostgreSQL) that stores conversations and messages so state survives a restart, instead of living only in the in-memory `messages` list.

**Learn** (~1 week)
- Relational databases: tables, rows, columns, primary/foreign keys, relationships, queries, indexes, transactions, persistence
- SQL: `SELECT`/`INSERT`/`UPDATE`/`DELETE`/`WHERE`/`JOIN`/`GROUP BY`/`ORDER BY`
- Data modeling for Conversation, Message, User, Metadata — and why schema design matters
- Indexes: what scanning without one costs vs. the storage/write tradeoff of adding one

**Resources**
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SQLBolt](https://sqlbolt.com/)

**Implement**
- [ ] Design the Conversation/Message schema
- [ ] Persist every message to PostgreSQL
- [ ] Load conversation history on restart
- [ ] Basic queries (recent messages, by conversation)

## Subtask: Vector retrieval

pgvector-backed retrieval of relevant prior interactions, plus a bounded experiment comparing flat vector retrieval against a summary-buffer approach on the same test queries.

**Learn** (~1 week)
- Information retrieval: embeddings, vector spaces conceptually, similarity, nearest-neighbor search, ranking, precision/relevance tradeoffs
- Data modeling for Embedding and Retrieved memory
- Indexes, applied to vector search specifically (exact search first, before approximate)

**Resources**
- [pgvector](https://github.com/pgvector/pgvector) — start with exact vector search, don't jump to approximate indexing
- [Embeddings — Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/embeddings)

**Implement**
- [ ] 768-dimensional embeddings via `nomic-embed-text` (Ollama embeddings)
- [ ] Store embeddings in pgvector
- [ ] Retrieval of relevant prior interactions
- [ ] Bounded experiment: flat vector retrieval vs. summary-buffer, same test queries, measure → choose → stop

---

## Tech stack learned

- PostgreSQL
- SQL
- pgvector
- nomic-embed-text
- Ollama embeddings
- Python PostgreSQL client

## Prerequisites

Basic Python.

No database expertise required beforehand.

## Exit condition

The agent persists information across restarts and retrieves useful prior information.

I can explain relational storage, indexes, embeddings, and retrieval independently of PostgreSQL/pgvector syntax.

---

# Phase 3 — Multi-step planning — M

## Subtask: Multi-step control flow

Extend the agent loop to handle tasks that need multiple tools in sequence (e.g. `list_directory` → identify PDFs → summarize each → aggregate), instead of the current single-tool-then-done loop.

**Learn** (~3–4 days)
- State machines: state → transition → new state; starting/intermediate/terminal/failure states; map the agent loop onto this model
- Software architecture: task decomposition, intermediate state, composable operations, planner/executor separation, control flow

**Resources**
- [Game Programming Patterns — State](https://gameprogrammingpatterns.com/state.html) — focus on the pattern, not game dev
- [ReAct paper](https://arxiv.org/abs/2210.03629) — revisit, now comparing the paper's loop to the actual system you built

**Implement**
- [ ] Loop supports calling more than one tool per task before a Final Answer
- [ ] Explicit intermediate state between tool calls
- [ ] Represent the fixed example flow (`list_directory` → summarize → aggregate) as explicit state transitions

## Subtask: `draft_email` + failure handling

A `draft_email` tool that drafts only and never sends — the project's first draft-only external-action boundary — plus reliability handling for the failure case where one step in a multi-step task fails.

**Learn** (~2–3 days)
- Software architecture: Recovery — putting the control-flow subtask's model into practice for one failing step
- Reliability: detects failure, preserves state, retries appropriately, avoids infinite loops, terminates cleanly (step A succeeds → step B succeeds → step C fails)

**Resources**
- (project-internal — applies the state-machine and reliability material from the control-flow subtask above to one concrete failure case)

**Implement**
- [ ] `draft_email` tool (drafts only, never sends)
- [ ] One controlled failure case handled without an infinite loop
- [ ] Clean termination on that failure

---

## Tech stack learned

Mostly existing stack:

- Python
- Ollama
- ReAct loop
- Tool registry

Potentially:

- `dataclasses`
- Pydantic

Only if justified.

## Prerequisites

- Phase 1 reliable
- Comfortable with state and loops

## Exit condition

The agent completes a fixed multi-tool task, handles one controlled failure, and terminates correctly.

I can represent its execution as explicit state transitions.

---

# Phase 4 — Isolation sandbox — L

## Motivation

Learn where the security boundary sits for agent tool execution. This is the largest systems-foundation phase. Start with Docker; do NOT default to SaaS sandbox APIs.

## Subtask: Containerized execution & mounts

Run risky tool execution inside a Docker container instead of directly on the host, with a read-only mount for the project and an explicit writable scratch directory for anything the agent needs to write.

**Learn** (~1 week)
- Containers mental model: container ≠ tiny VM, container ≈ isolated Linux process(es)
- Operating systems: programs vs. processes, PID, parent/child processes, process lifecycle, system calls conceptually
- Docker: images, Dockerfiles, bind mounts, volumes

**Resources**
- [iximiuz Labs](https://labs.iximiuz.com) — PRIMARY; focus on containers, container images, filesystems
- [Docker Get Started](https://docs.docker.com/get-started/)
- Liz Rice — **Containers From Scratch** (watch after basic Docker familiarity)

**Implement**
- [ ] Run tool execution inside a Docker container
- [ ] Read-only mount for the project directory
- [ ] Explicit writable scratch directory

## Subtask: Resource limits

CPU, memory, and process limits, plus an execution timeout, so a runaway or malicious tool call can't consume unlimited host resources.

**Learn** (~3–4 days)
- cgroups: resources a process can consume
- Operating systems: scheduling conceptually, virtual memory conceptually, signals

**Resources**
- [iximiuz Labs](https://labs.iximiuz.com) — Linux processes, namespaces
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — CPU scheduling, address spaces, virtual memory overview (not cover-to-cover)

**Implement**
- [ ] CPU limits
- [ ] Memory limits
- [ ] Process limits
- [ ] Execution timeout

## Subtask: Network isolation

Restricted or no network access for the container, plus controlled environment variables, so a sandboxed tool can't reach the host network or leak credentials through the environment.

**Learn** (~3–4 days)
- Networking: network interfaces, IP addresses, ports, localhost, TCP, UDP conceptually, client/server, DNS, NAT conceptually, container networking
- Environment variables (the OS concept behind the "controlled environment variables" implement item below)
- Security: trust boundaries, least privilege, attack surface, capabilities

**Resources**
- [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet/) — networks, IP, ports, TCP, client/server
- [iximiuz Labs](https://labs.iximiuz.com) — networking

**Implement**
- [ ] Restricted/no network for the sandboxed container
- [ ] Controlled environment variables (no credential leakage)

## Subtask: Isolation model comparison

A conceptual comparison of standard containers, hardened containers, gVisor, and microVMs, so the choice of Docker for this phase is a deliberate tradeoff rather than a default.

**Learn** (~3–4 days)
- Linux internals: `/proc`, users, permissions, mounts, namespaces, cgroups
- Security: isolation, sandboxing, host vs. container boundary

**Resources**
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — processes, process API
- [iximiuz Labs](https://labs.iximiuz.com) — namespaces
- Liz Rice — **Containers From Scratch**

**Implement**
- [ ] Written comparison: standard containers vs. hardened containers vs. gVisor vs. microVMs
- [ ] Explanation of which Linux mechanisms actually enforce the sandbox's restrictions

---

## Tech stack learned

- Linux
- Docker
- Dockerfiles
- Images
- Containers
- Bind mounts
- Volumes
- Container networking
- Resource controls

## Prerequisites

Phase 1 Linux knowledge.

Before sandbox implementation, understand at least:

```
process
PID
signal
IP
port
TCP
image
container
mount
namespace
cgroup
```

## Exit condition

Untrusted execution runs in an isolated container with:

- No arbitrary host filesystem access
- No host credentials
- Restricted/no network
- CPU limits
- Memory limits
- Process limits
- Timeout

Attempts to cross the intended boundary fail.

I can explain which Linux mechanisms actually enforce those restrictions.

---

# Phase 5 — Evaluation harness — L

Build this BEFORE parallelism.

## Subtask: Eval task harness

Tasks with checkable, pass/fail outcomes that one command can run, so changes get measured instead of eyeballed.

**Learn** (~4–5 days)
- Software testing: unit/integration/end-to-end tests, fixtures, assertions, regression tests, test isolation
- Experimental design: baseline → controlled change → measurement → comparison — matters especially because LLM systems are probabilistic

**Resources**
- [pytest — Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
- [Software Engineering at Google — Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html)

**Implement**
- [ ] Task definitions with checkable outcomes
- [ ] One command runs the full suite
- [ ] Pass/fail + aggregate score reporting

## Subtask: Trajectory recording & comparisons

Full recording of every model response, tool call, and trajectory, so runs can be diffed and compared across prompts, models, and agent implementations.

**Learn** (~4–5 days)
- Reliability engineering: what failed, where, why, can I reproduce it, did this change make things better

**Resources**
- [Software Engineering at Google — Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html)

**Implement**
- [ ] Record every model response, tool call, complete trajectory, timing, errors
- [ ] Support comparisons between prompts, models, and agent implementations
- [ ] Structured JSON logs

## Subtask: OpenTelemetry tracing

Map agent steps to OpenTelemetry spans, so a run's execution path is visible as a trace, not just a log line.

**Learn** (~4–5 days)
- Observability: logs (individual events) vs. metrics (aggregate measurements) vs. traces (path of work through a system)
- Trace, span, parent/child spans, context propagation, correlation IDs

**Resources**
- [OpenTelemetry docs](https://opentelemetry.io/docs/)
- [OpenTelemetry — Python](https://opentelemetry.io/docs/languages/python/)
- [OpenTelemetry — Tracing](https://opentelemetry.io/docs/concepts/signals/traces/)

**Implement**
- [ ] Map agent steps to OTel spans where appropriate
- [ ] Trace visualization for a run
- [ ] Failure location visible in the trace

---

## Tech stack learned

- pytest
- Python logging
- Structured JSON logs
- OpenTelemetry
- Trace visualization

## Prerequisites

Basic testing concepts.

## Exit condition

One command runs the evaluation suite and reports:

- Task pass/fail
- Aggregate score
- Model responses
- Tool calls
- Failure location
- Trace

A change can be objectively compared against a saved baseline.

---

# Phase 6 — Parallel orchestration — LAST — L

## Motivation

Learn concurrency, resource management, and orchestration. Phase 5 must exist first.

## Subtask: Async fan-out & result collection

Fan out N agent runs concurrently using `asyncio`, and collect their results, instead of running the evaluation workload one task at a time.

**Learn** (~1 week)
- Concurrency: sequential vs. concurrent vs. parallel; threads, processes, coroutines, event loops, async I/O, tasks, futures, queues, semaphores, synchronization, race conditions, deadlocks conceptually, backpressure

**Resources**
- [asyncio conceptual overview](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html) — read before using asyncio heavily
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html) — coroutines, tasks, task groups, queues, synchronization

**Implement**
- [ ] Fan out N agent runs with `asyncio`
- [ ] Collect results from concurrent runs
- [ ] Process/container pools where appropriate

## Subtask: Timeouts & partial failure

Timeouts at three levels — tool call, task loop, sandbox lifetime — plus handling for partial failure across a batch of concurrent runs, so one hung or failed task doesn't take down the whole batch.

**Learn** (~1 week)
- Distributed-systems foundations: workers, scheduling, partial failure, timeouts, retries, result aggregation, idempotency conceptually, backpressure — the system stays local, but the failure patterns start resembling distributed systems

**Resources**
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html) — cancellation, timeouts

**Implement**
- [ ] Tool-call timeout
- [ ] Task-loop timeout
- [ ] Sandbox-lifetime timeout
- [ ] Partial-failure handling and result aggregation across a batch

## Subtask: Resource measurement

Measure local resource limits (don't guess) so the chosen concurrency level is justified by data — CPU, RAM, GPU, VRAM, latency, throughput, and where the actual bottleneck sits.

**Learn** (~1 week)
- Operating systems, deepened: processes, threads, scheduling, context switching, resource contention
- Computer systems: CPU/RAM/GPU/VRAM/storage/network; latency, throughput, utilization, bottlenecks, memory pressure

**Resources**
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — concurrency, threads, locks, condition variables
- [iximiuz Labs](https://labs.iximiuz.com) — relevant Linux/process/resource-management labs

**Implement**
- [ ] Measure runtime, per-task latency, throughput, success/failure rate
- [ ] Measure RAM/VRAM usage (Linux + GPU monitoring)
- [ ] Justify the chosen concurrency limit with the measurements

---

## Tech stack learned

- Python `asyncio`
- Task groups
- Queues
- Semaphores
- Process pools
- Docker
- Ollama
- Linux monitoring
- GPU monitoring

## Prerequisites

Understand:

- Processes
- Threads conceptually
- CPU/RAM
- GPU/VRAM
- Blocking vs non-blocking I/O

Phase 5 must exist first.

## Exit condition

A fixed evaluation workload runs with configurable concurrency.

Measure:

- Runtime
- Per-task latency
- Throughput
- Success rate
- RAM
- VRAM
- Failure rate

The chosen concurrency limit is justified by measurements.

---

# MVP completion criteria

The project is complete after Phase 6 when it contains:

- Scratch-built agent loop
- Multiple tools
- Safe filesystem interaction
- Persistent memory
- Vector retrieval
- Multi-step execution
- Draft-only external-action boundary
- Sandboxed execution
- Evaluation suite
- Tracing
- Bounded concurrency
- Resource measurements
- Architecture/design documentation

At this point, stop treating the core project as unfinished.

Everything below is optional specialization.

---

# Optional Phase A — LangChain / LangGraph — M

## Trigger

Scratch implementation is complete enough to make comparison meaningful.

May start in parallel once Phase 3 is done (see Industry-currency lane above) — does not require the full MVP, but stays time-boxed and never displaces Phases 4–6.

## Subtask: Port to LangChain/LangGraph

Port one representative workflow (scratch implementation vs. framework implementation) to understand what an agent framework abstracts.

**Learn** (~4 days)
- Framework design: abstraction, interfaces, inversion of control, framework vs. library, state graphs, abstraction leakage

**Resources**
- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)

**Implement**
- [ ] Pick one representative workflow already built from scratch
- [ ] Rebuild it in LangChain/LangGraph

## Subtask: Architectural comparison write-up

A written comparison answering what code disappeared, who now owns the control loop, where state is stored, how failures are represented, and what control was gained vs. lost by moving to the framework.

**Learn** (~2–3 days)
- Same framework-design questions, applied specifically to the two implementations side by side: What code disappeared? Who now owns the control loop? Where is state stored? How are failures represented? What control was gained vs. lost?

**Resources**
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

**Implement**
- [ ] Written architectural comparison (scratch vs. framework)

---

## Tech stack

- LangChain
- LangGraph
- Ollama

## Exit condition

The same meaningful workflow exists in scratch and framework versions with a written architectural comparison.

---

# Optional Phase B — Langfuse — M

## Trigger

Phase 5 exists.

## Subtask: Langfuse integration & comparison

Wire Langfuse alongside the existing OpenTelemetry-based evaluation/tracing system to compare a specialized LLM observability platform against what was hand-built in Phase 5.

**Learn** (~1 week)
- Production observability, deepened: distributed tracing, telemetry, trace storage, correlation, evaluation datasets, experiment tracking

**Resources**
- [Langfuse docs](https://langfuse.com/docs)
- [Langfuse — Observability overview](https://langfuse.com/docs/observability/overview)

**Implement**
- [ ] Wire Langfuse into the existing evaluation harness
- [ ] Run the same execution through both Langfuse and the custom system
- [ ] Document the tradeoffs between the two

---

## Tech stack

- Langfuse
- OpenTelemetry
- Existing evaluation harness

## Exit condition

The same execution is inspectable through both systems and their tradeoffs are documented.

---

# Optional Phase C — Remote agent control — M/L

## Trigger

I want to operate the agent while away from the machine running it.

Goal shape: phone/laptop → secure network → Agent API → Agent runtime → Ollama + sandbox.

## Subtask: FastAPI agent API

A FastAPI service in front of the agent runtime supporting submit task, task ID, status, and result — so a task can be submitted and polled instead of requiring a live terminal session.

**Learn** (~1 week)
- Backend systems: client/server architecture, APIs, request/response, authentication, authorization, long-running jobs, idempotency, error codes
- Networking basics: application layer, HTTP, transport layer, TCP, ports

**Resources**
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/)
- Computer Networking: A Top-Down Approach — application layer, HTTP, transport layer, TCP, network layer basics
- [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet/) — free supplement

**Implement**
- [ ] Submit-task endpoint returning a task ID
- [ ] Status endpoint
- [ ] Result endpoint

## Subtask: Secure remote access

Cancellation support plus a private network path (Tailscale or equivalent, SSH) so the agent API is reachable from another device without exposing it publicly.

**Learn** (~4–5 days)
- Networking, studied more systematically: network layers, IP, routing, DNS, NAT, firewalls, TLS

**Resources**
- [Tailscale docs](https://tailscale.com/kb)
- [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet/)

**Implement**
- [ ] Cancellation endpoint
- [ ] Private network path (Tailscale or equivalent / SSH) — no public exposure of the privileged agent

---

## Tech stack

- FastAPI
- Uvicorn
- SSH
- Tailscale or equivalent
- Docker
- Linux

## Exit condition

Another device can securely submit, monitor, retrieve, and cancel tasks without exposing the privileged agent publicly.

---

# Optional Phase D — Linux and container internals — L

## Trigger

Operating systems/container isolation becomes an area I want to understand deeply.

## Subtask: Namespaces & `/proc`

Create namespaces manually and inspect container processes from the host and via `/proc`, to see directly what a namespace does and doesn't hide.

**Learn** (~1 week)
- System calls, processes, `/proc`, signals, file descriptors
- Namespaces: mount namespaces, PID namespaces, network namespaces

**Resources**
- [iximiuz Labs](https://labs.iximiuz.com) — primary hands-on
- [Linux Insides](https://0xax.gitbooks.io/linux-insides/)

**Implement**
- [ ] Create namespaces manually
- [ ] Inspect container processes from the host
- [ ] Inspect `/proc` for a running container

## Subtask: cgroups & resource limits

Apply cgroup limits directly (outside of Docker's abstraction) to see the actual mechanism Phase 4's resource limits relied on.

**Learn** (~2–3 days)
- cgroups, virtual memory conceptually

**Resources**
- [iximiuz Labs](https://labs.iximiuz.com)
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)

**Implement**
- [ ] Apply cgroup limits manually
- [ ] Compare mount namespaces

## Subtask: Container runtimes comparison

Create network namespaces, run rootless containers, and compare Docker and Podman, to reproduce a simplified container-like environment from Linux primitives and see what a runtime adds on top.

**Learn** (~1 week)
- Capabilities, seccomp, overlay filesystems, OCI, container runtimes, rootless containers

**Resources**
- [Podman docs](https://docs.podman.io/)
- Liz Rice — Containers From Scratch

**Implement**
- [ ] Create network namespaces
- [ ] Run rootless containers
- [ ] Compare Docker and Podman

---

## Tech stack

- Linux
- Docker
- Podman
- `unshare`
- `nsenter`
- `/proc`
- cgroups

## Exit condition

I can explain what Docker does beneath its CLI and reproduce a simplified container-like environment using Linux primitives.

---

# Optional Phase E — Kubernetes — L

## Trigger

A genuine orchestration problem exists — multiple services, multiple workers, replicas, restart requirements, or deployment management.

## Subtask: Core objects

Cluster, control plane, node, pod, deployment, and service — the objects needed to run one component of the agent system on Kubernetes at all.

**Learn** (~1 week)
- Distributed systems: desired state, reconciliation, scheduling, service discovery
- Cluster, control plane, node, pod, deployment, service, scheduler

**Resources**
- [iximiuz Labs](https://labs.iximiuz.com)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/)
- [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

**Implement**
- [ ] Set up a local cluster (kind or minikube)
- [ ] Deploy one component as a Pod/Deployment/Service

## Subtask: Config & state

ConfigMap, Secret, and PersistentVolume — how configuration and state are managed separately from the container image.

**Learn** (~3–4 days)
- Distributed configuration, failure recovery, replication

**Resources**
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/)
- [Interactive practice — killercoda](https://killercoda.com/kubernetes)

**Implement**
- [ ] ConfigMap for configuration
- [ ] Secret for sensitive values
- [ ] PersistentVolume for state

## Subtask: Operations

Scheduler behavior, health checks, rolling deployment, and scaling — the operational concerns Kubernetes handles beyond just running containers.

**Learn** (~3–4 days)
- Health checking, replication, scheduling (applied operationally)

**Resources**
- [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)
- [Interactive practice — killercoda](https://killercoda.com/kubernetes)

**Implement**
- [ ] Health checks configured
- [ ] Rolling deployment
- [ ] Scaling

---

## Tech stack

- Kubernetes
- `kubectl`
- YAML
- kind or minikube

## Exit condition

One meaningful component of the agent system runs on a local Kubernetes cluster and I can explain what Kubernetes provides beyond running Docker containers manually.

---

# Optional Phase F — Cloud deployment — L

## Trigger

I want deeper infrastructure/cloud experience. Goal: deploy the system or part of it onto a remote Linux machine. Choose ONE cloud provider (AWS, GCP, or Azure).

## Subtask: Provision cloud infra

A VM, network, and security boundary on the chosen cloud provider — the infrastructure the deployment will actually run on.

**Learn** (~1 week)
- Infrastructure and networking: virtual machines, virtual networks, subnets conceptually, routing, firewalls, DNS, persistent storage, IAM, secrets

**Resources**
- [AWS Skill Builder](https://skillbuilder.aws/) — EC2, VPC, security groups, IAM, storage

**Implement**
- [ ] Provision a VM
- [ ] Configure VPC/security groups
- [ ] IAM + secrets set up

## Subtask: Infra as code / deploy

Terraform (or equivalent) to make the deployment reproducible, plus the actual service management (Docker Compose, systemd, Nginx/Caddy) running the agent on the remote machine.

**Learn** (~1 week)
- Service management

**Resources**
- [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials)
- [Docker Compose — Getting Started](https://docs.docker.com/compose/gettingstarted/)

**Implement**
- [ ] Infrastructure defined as code (Terraform)
- [ ] Service running via Docker Compose/systemd
- [ ] Reverse proxy (Nginx/Caddy) if needed

---

## Tech stack

Choose ONE:

- AWS
- GCP
- Azure

Potential additions:

- Terraform
- Docker Compose
- systemd
- Nginx/Caddy

## Exit condition

The remote system can be recreated from documentation or infrastructure code without unexplained manual configuration.

---

# Optional Phase G — CI/CD — M

## Trigger

The project has tests, evaluation, a container build, and a deployable artifact.

Pipeline shape: `git push` → tests → eval subset → build container → publish image → optional deployment.

## Subtask: CI pipeline

Tests and an eval subset running automatically on every push, so a change is verified before it's trusted.

**Learn** (~3–4 days)
- Software delivery: build pipelines, continuous integration, environment separation, secrets in automation

**Resources**
- [GitHub Actions docs](https://docs.github.com/en/actions)

**Implement**
- [ ] Tests run on push
- [ ] Eval subset runs on push

## Subtask: Container build & publish

Build the container image and publish it, with optional deployment, so a clean commit produces a versioned, deployable artifact.

**Learn** (~2–3 days)
- Software delivery: continuous delivery, artifacts, versioning, reproducible builds

**Resources**
- [Docker Build docs](https://docs.docker.com/build/)

**Implement**
- [ ] Build container image in CI
- [ ] Publish image to a container registry
- [ ] Optional deployment step

---

## Tech stack

- GitHub Actions
- Docker
- Container registry

## Exit condition

A clean commit automatically produces a tested and versioned artifact.

---

# Optional Phase H — Multi-agent systems — L

## Trigger

One agent already performs reliably. Never add agents to compensate for a broken single-agent architecture.

## Subtask: Coordinator + specialized agents

Build a coordinator dispatching to specialized agents, to compare against the existing single-agent-plus-tools architecture.

**Learn** (~1 week)
- Coordination: message passing, task assignment, shared state, partial failures, communication overhead
- AI systems: delegation, specialization, routing, agent communication, coordination overhead

**Resources**
- **Designing Multi-Agent Systems** — Victor Dibia (primary)
- [LangGraph — Workflows & Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) (supplement)

**Implement**
- [ ] Coordinator + at least two specialized agents
- [ ] Same workload runnable through both single-agent and multi-agent paths

## Subtask: Single vs. multi-agent experiment

Measure single agent vs. multi-agent on success rate, latency, model calls, resource use, failure rate, and complexity, to get actual evidence rather than an assumption that multi-agent is better.

**Learn** (~2–3 days)
- Same coordination/AI-systems material, applied to interpreting the measurement results

**Resources**
- **Designing Multi-Agent Systems** — Victor Dibia

**Implement**
- [ ] Run the same workload single-agent and multi-agent
- [ ] Measure success rate, latency, model calls, resource use, failure rate, complexity
- [ ] Written verdict on whether the added complexity was justified

---

## Tech stack

Start with existing scratch implementation.

LangGraph may be used if Optional Phase A is already complete.

## Exit condition

There is measurable evidence that multi-agent coordination helps at least one workload enough to justify its complexity.

---

# Optional Phase I — MLOps / model serving — L

## Trigger

I want deeper ML engineering/MLOps experience — stop treating local inference as a black box, study the model as a deployed system.

## Subtask: Measure serving performance

Measure model latency, throughput, VRAM, RAM, and behavior under concurrent requests for the existing Ollama setup.

**Learn** (~1 week)
- Systems performance: latency, throughput, utilization, saturation, bottlenecks, memory, batching, queueing
- GPU systems conceptually: GPU vs. CPU, GPU memory, model weights, KV cache, memory bandwidth, batch size, concurrency

**Resources**
- [NVIDIA CUDA documentation](https://docs.nvidia.com/cuda/) — conceptual material first
- [Hugging Face documentation](https://huggingface.co/docs)
- Systems Performance — Brendan Gregg (latency, throughput, utilization, saturation, profiling sections)

**Implement**
- [ ] Measure model latency and throughput
- [ ] Measure VRAM/RAM usage
- [ ] Measure behavior under concurrent requests

## Subtask: Serving comparison

Compare Ollama against another inference server (e.g. vLLM), only when there's a specific question being tested — not as a default exercise.

**Learn** (~2–3 days)
- Same systems-performance and GPU material, applied to interpreting the comparison

**Resources**
- Same as above

**Implement**
- [ ] Define the specific question being tested before running the comparison
- [ ] Ollama vs. another inference server on that question

---

## Tech stack

Potentially:

- Ollama
- vLLM or another serving system
- NVIDIA tools
- Docker
- OpenTelemetry

## Exit condition

I can measure and explain how serving configuration affects:

- Latency
- Throughput
- RAM
- VRAM
- Concurrency
- Reliability

---

# Foundation coverage after MVP

Completing the MVP should provide meaningful practical foundations in:

## Programming and software engineering

- Program architecture
- State
- Interfaces
- Error handling
- Parsing
- Testing
- Reliability
- Git

## Linux and operating systems

- Filesystems
- Permissions
- Processes
- Signals
- Resource management
- Isolation
- Namespaces
- cgroups

## Databases

- Relational model
- SQL
- Data modeling
- Indexes
- Persistence

## Information retrieval

- Embeddings
- Similarity
- Vector retrieval
- Ranking

## Networking

- Client/server
- IP
- Ports
- TCP
- HTTP
- Basic container networking

## Security

- Trust boundaries
- Least privilege
- Sandboxing
- Filesystem isolation
- Network isolation

## Testing and observability

- Unit/integration/E2E testing
- Regression testing
- Logs
- Metrics
- Traces
- OpenTelemetry

## Concurrency and systems

- Processes
- Threads conceptually
- Async I/O
- Event loops
- Queues
- Synchronization
- Resource contention
- CPU/RAM/GPU/VRAM
- Latency and throughput

## Distributed-systems introduction

- Workers
- Scheduling
- Timeouts
- Retries
- Partial failures
- Result aggregation

---

# Foundations intentionally handled elsewhere

## Data structures and algorithms

Handled separately through LeetCode and dedicated DSA study.

This project can use data structures when appropriate, but DSA study is not part of its scope.

---

# Core learning resources

## Systems / Linux / containers / networking

### iximiuz Labs

https://labs.iximiuz.com

Primary hands-on systems resource.

---

## Operating systems

### Operating Systems: Three Easy Pieces

https://pages.cs.wisc.edu/~remzi/OSTEP/

---

## Linux

### Linux Journey

https://linuxjourney.com/

### The Linux Command Line — William Shotts

https://linuxcommand.org/tlcl.php

---

## Networking

### Computer Networking: A Top-Down Approach

Primary theoretical resource.

### Beej’s Guide to Network Concepts

https://beej.us/guide/bgnet/

Free practical supplement.

---

## Databases

### PostgreSQL Tutorial

https://www.postgresql.org/docs/current/tutorial.html

### SQLBolt

https://sqlbolt.com/

---

## Multi-agent systems

### Designing Multi-Agent Systems — Victor Dibia

Primary resource for the optional multi-agent deep dive.

Reading may happen earlier.

Implementation does not jump the sequence.

---

# Standing guardrails

- **Reading never gates building.** Reading and building are parallel lanes.
- **Foundations are different from tools.** Spend time understanding OS, networking, databases, concurrency, and systems concepts. Do not spend equivalent time memorizing Docker, Kubernetes, or framework APIs.
- **Spine first.** Get a dumb end-to-end version running, then deepen one component at a time.
- **Theory gets applied.** A foundational concept should be connected to an experiment or project behavior whenever possible.
- **Every deepening gets a written exit condition decided in advance.**
- **Commit often.** A working checkpoint gets committed before the next change.
- **Anti-displacement flag.** Elaborate planning or infrastructure-building can substitute for shipping. If I’m building infrastructure instead of shipping a feature or learning the underlying concept, that gets called.
- **AI in tutor role, not coder.** I write the load-bearing code myself.
- **Verify fast-moving facts.** Versions, pricing, APIs, libraries, and tool capabilities must be checked against current documentation.
- **MVP means stop.** After Phase 6 satisfies its exit condition, the core project is complete.
- **Learn abstractions after primitives.** LangChain, LangGraph, Langfuse, Docker, Kubernetes, and similar tools should make more sense because I understand the concepts underneath them.
- **Do not collect technologies.** Every technology must solve a concrete problem or expose a useful concept.
- **Prefer measurement to intuition.** Especially for memory, evaluation, concurrency, serving, and resource limits.
- **Remote execution increases the security bar.** A remotely reachable agent with filesystem or execution tools is privileged infrastructure.
- **Industry currency is parallel and time-boxed.** The Industry-currency lane keeps hosted APIs, frameworks, and industry tooling in view without becoming a second project. It is the first thing cut under the anti-displacement flag — the scratch build never is.

---

# Parked / not in scope yet

Nothing beyond Phase 6 is required.

Optional phases become active only when I deliberately choose a deep-dive direction.

New ideas do not jump the queue.

Examples:

- Fine-tuning
- Production Kubernetes
- Multiple cloud providers
- Hosted sandbox APIs
- Complex frontend
- Autonomous email sending
- Autonomous deployment
- Large multi-agent swarms
- Redis
- Kafka
- Ray
- Distributed inference
- Custom model training

Before promoting anything:

> What concrete limitation of the current system does this solve, and what CS or systems concept am I trying to understand by adding it?
>