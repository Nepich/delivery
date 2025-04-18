
import asyncio
from that_depends import Provide
from api.dic import DIContainer
from api.scheduler import Scheduler


async def start_sheduler(scheduler: Scheduler = Provide[DIContainer.scheduler.sync_resolve()]):
    scheduler.start()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_sheduler())
    loop.run_forever()