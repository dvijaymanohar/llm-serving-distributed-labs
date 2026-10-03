import asyncio, random, statistics, time

async def fake_generate(tokens=16, first_ms=40, token_ms=8):
    await asyncio.sleep(first_ms/1000)
    yield 0
    for i in range(1,tokens):
        await asyncio.sleep((token_ms+random.uniform(-2,2))/1000)
        yield i

async def main():
    start=time.perf_counter(); stamps=[]
    async for _ in fake_generate():
        stamps.append(time.perf_counter())
    ttft=(stamps[0]-start)*1000
    itl=[(b-a)*1000 for a,b in zip(stamps,stamps[1:])]
    print({"ttft_ms":ttft,"itl_median_ms":statistics.median(itl),"itl_p95_ms":sorted(itl)[int(.95*(len(itl)-1))],"tokens":len(stamps)})
asyncio.run(main())
