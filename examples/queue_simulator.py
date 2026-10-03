import argparse, asyncio, random, statistics, time

async def worker(q,service_ms):
    while True:
        item=await q.get()
        if item is None: q.task_done(); return
        enqueued,fut=item
        await asyncio.sleep(service_ms/1000)
        if not fut.done(): fut.set_result((time.perf_counter()-enqueued)*1000)
        q.task_done()

async def run(requests,concurrency,queue_size,service_ms):
    q=asyncio.Queue(maxsize=queue_size)
    workers=[asyncio.create_task(worker(q,service_ms)) for _ in range(concurrency)]
    lat=[]; rejected=0
    for _ in range(requests):
        fut=asyncio.get_running_loop().create_future()
        try:
            q.put_nowait((time.perf_counter(),fut))
            lat.append(fut)
        except asyncio.QueueFull:
            rejected+=1
        await asyncio.sleep(random.random()*0.001)
    values=await asyncio.gather(*lat) if lat else []
    await q.join()
    for _ in workers: await q.put(None)
    await asyncio.gather(*workers)
    values.sort()
    def pct(p): return values[min(len(values)-1,int(p*(len(values)-1)))] if values else float("nan")
    print({"accepted":len(values),"rejected":rejected,"p50_ms":pct(.50),"p95_ms":pct(.95),"p99_ms":pct(.99)})

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--requests",type=int,default=500)
    p.add_argument("--workers",type=int,default=4); p.add_argument("--queue",type=int,default=64)
    p.add_argument("--service-ms",type=float,default=10)
    a=p.parse_args(); asyncio.run(run(a.requests,a.workers,a.queue,a.service_ms))
