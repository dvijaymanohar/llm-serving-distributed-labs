# LLM Serving & Distributed Labs

Hands-on serving-system experiments for streaming metrics, queueing, batching, concurrency, overload, reliability, and distributed GPU concepts.

## Sequence
model/tokenizer load → streaming generation → TTFT/ITL → batch/concurrency sweep → KV-cache effects → runtime comparison → bounded queue/backpressure → health/readiness → metrics → retries/overload → tensor parallel/NCCL → RDMA/scale-out concepts.

The default examples use a synthetic worker so queueing/reliability mechanics can run without a large model. Replace the worker with a real open LLM runtime when hardware permits.
