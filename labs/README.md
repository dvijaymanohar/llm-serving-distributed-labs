# Serving-system labs

These examples intentionally separate serving mechanics from a heavyweight model runtime.

```bash
python examples/streaming_metrics.py
python examples/dynamic_batcher.py
python examples/queue_simulator.py --requests 1000 --workers 4 --queue 64 --service-ms 10
python examples/retry_storm.py
python examples/readiness_state.py
python benchmarks/load_sweep.py
```

Then replace the synthetic worker with a real LLM runtime.

Experiments:
- TTFT vs ITL;
- max-batch vs max-wait trade-off;
- queue capacity and admission control;
- concurrency through saturation;
- retries under overload;
- health vs readiness during model initialization;
- worker crash/restart;
- long-running soak;
- canary comparison with explicit rollback thresholds.
