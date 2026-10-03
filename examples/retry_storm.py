import asyncio, random, statistics, time

async def flaky_service(load):
    await asyncio.sleep(0.005)
    if random.random() < min(.9, load/100): raise RuntimeError("overloaded")
    return 1

async def request(max_retries,backoff):
    start=time.perf_counter(); attempts=0
    while True:
        attempts+=1
        try:
            await flaky_service(80); return True,attempts,(time.perf_counter()-start)*1000
        except RuntimeError:
            if attempts>max_retries:return False,attempts,(time.perf_counter()-start)*1000
            await asyncio.sleep(backoff*attempts)

async def run(retries):
    out=await asyncio.gather(*(request(retries,.002) for _ in range(200)))
    attempts=sum(x[1] for x in out); success=sum(x[0] for x in out)
    lat=[x[2] for x in out]
    print({"max_retries":retries,"successes":success,"total_attempts":attempts,
           "median_ms":statistics.median(lat),"p95_ms":sorted(lat)[189]})

asyncio.run(run(0)); asyncio.run(run(3))
