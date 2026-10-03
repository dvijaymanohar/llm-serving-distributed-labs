import asyncio, random, statistics, time

class DynamicBatcher:
    def __init__(self,max_batch=8,max_wait_ms=5):
        self.q=asyncio.Queue(); self.max_batch=max_batch; self.max_wait=max_wait_ms/1000
    async def submit(self,x):
        fut=asyncio.get_running_loop().create_future(); await self.q.put((x,fut,time.perf_counter())); return await fut
    async def run(self):
        while True:
            first=await self.q.get()
            if first is None: return
            batch=[first]; deadline=time.perf_counter()+self.max_wait
            while len(batch)<self.max_batch:
                timeout=deadline-time.perf_counter()
                if timeout<=0: break
                try: batch.append(await asyncio.wait_for(self.q.get(),timeout))
                except asyncio.TimeoutError: break
            await asyncio.sleep(0.003+0.001*len(batch))  # synthetic batched compute
            now=time.perf_counter()
            for x,fut,enq in batch: fut.set_result((x*2,(now-enq)*1000,len(batch)))

async def main():
    b=DynamicBatcher(); worker=asyncio.create_task(b.run())
    async def client(i):
        await asyncio.sleep(random.random()*0.02); return await b.submit(i)
    out=await asyncio.gather(*(client(i) for i in range(100)))
    await b.q.put(None); await worker
    lat=[x[1] for x in out]; sizes=[x[2] for x in out]
    print({"latency_median_ms":statistics.median(lat),"latency_p95_ms":sorted(lat)[94],
           "mean_batch_size":statistics.mean(sizes),"max_batch_size":max(sizes)})
asyncio.run(main())
