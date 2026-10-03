import asyncio, statistics, time

class AdmissionController:
    def __init__(self,max_inflight=8):
        self.sem=asyncio.Semaphore(max_inflight)
        self.rejected=0
    async def try_run(self,coro_factory,timeout_s=0.002):
        try:
            await asyncio.wait_for(self.sem.acquire(),timeout=timeout_s)
        except asyncio.TimeoutError:
            self.rejected+=1
            return None
        try:
            return await coro_factory()
        finally:
            self.sem.release()

async def service():
    await asyncio.sleep(.01)
    return 1

async def main():
    ctl=AdmissionController(8)
    start=time.perf_counter()
    out=await asyncio.gather(*(ctl.try_run(service) for _ in range(200)))
    elapsed=(time.perf_counter()-start)*1000
    accepted=sum(x is not None for x in out)
    print({"accepted":accepted,"rejected":ctl.rejected,"elapsed_ms":elapsed})
    print("Compare this bounded behavior with an unbounded queue under the same offered load.")
asyncio.run(main())
