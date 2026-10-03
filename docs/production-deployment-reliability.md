# Production deployment and reliability

## Architecture
request/API → bounded queue → batcher/scheduler → worker/runtime → accelerator → response/stream.

## Required concepts
- model latency vs service latency
- queueing and backpressure
- dynamic batching
- concurrency and saturation
- p50/p95/p99 latency
- health vs readiness
- metrics, logs, and traces
- timeouts
- bounded retries with backoff
- retry storms
- resource limits and failure isolation
- warm-up/caching
- canary deployment
- rollback criteria
- soak testing and long-running degradation
- scale-up vs scale-out

## Required experiments
1. Direct model call vs served request path.
2. Load sweep through saturation.
3. Bounded vs unbounded/admission-controlled queue.
4. Batch/concurrency sweep.
5. Retry-under-overload experiment.
6. Worker failure/restart.
7. Cold vs warm behavior.
8. Soak test.
9. Canary comparison with explicit rollback criteria.

Never improve average throughput by silently destroying tail latency or reliability.
