import asyncio

class Worker:
    def __init__(self): self.ready=False
    async def initialize(self):
        await asyncio.sleep(.1)  # model load / warm-up stand-in
        self.ready=True
    def health(self): return True
    def readiness(self): return self.ready

async def main():
    w=Worker()
    print("before init:",{"health":w.health(),"ready":w.readiness()})
    await w.initialize()
    print("after init:",{"health":w.health(),"ready":w.readiness()})
asyncio.run(main())
