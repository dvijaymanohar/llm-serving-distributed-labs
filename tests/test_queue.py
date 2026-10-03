import asyncio
from examples.queue_simulator import run

def test_small_queue_run():
    asyncio.run(run(requests=10,concurrency=2,queue_size=10,service_ms=0.1))
