# AI Usage Telemetry Platform

A portfolio project for collecting LLM usage events, estimating costs, and investigating reliability issues.

Status: learning scaffold. [Lab 01](labs/lab01/README.md) includes an in-memory mock HTTP API and a usage extraction exercise. No deployed services yet.

## Learning and delivery

- [Learning roadmap](docs/LEARNING_PLAN.md) — modules, practical cases and acceptance criteria (Russian).
- [Progress](docs/PROGRESS.md) — verified results and the next step.
- [Setup and handoff](docs/DEVELOPMENT.md) — another computer or AI assistant.
- [Assistant instructions](AGENTS.md) and [project context](docs/CONTEXT.md).

## Target architecture

```text
Mock / LLM API -> Python client -> durable usage events -> raw storage -> ClickHouse
                      |
                      +-> OpenTelemetry Collector -> trace backend

Raw storage -> Airflow / dbt -> analytical models -> dashboards
```

Components will be introduced incrementally. Initial exercises use synthetic data and mock APIs without paid LLM calls. Cost accounting must not rely on sampled traces.

## Planned portfolio evidence

Reproducible demo, tests, CI, architecture decisions, synthetic datasets, dashboards and incident reports. Implemented features and simulated workloads will be explicitly identified.
