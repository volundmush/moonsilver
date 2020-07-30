import esper
from honahlee.core import BaseService
from honahlee.utils.time import utcnow
import asyncio


class EngineService(BaseService):

    def __init__(self):
        super().__init__()
        self.world = esper.World()
        self.running = False

    def setup_processors(self):
        for k, v in self.app.classes['processors'].items():
            processor = v()
            self.world.add_processor(processor, priority=processor.proc_priority)

    def load_static_assets(self):
        pass

    def load_static_world(self):
        pass

    async def load_database_assets(self):
        pass

    def load_database_world(self):
        pass

    async def setup(self):
        self.setup_processors()
        self.load_static_assets()
        self.load_static_world()
        await self.load_database_assets()
        self.load_database_world()


    async def start(self):
        sess_srv = self.app.services['session']
        # Interval is a timedelta.
        interval = self.app.config.update_interval
        self.running = True
        last_timestamp = utcnow()
        current_timestamp = utcnow()
        while self.running:
            delta = current_timestamp - last_timestamp
            # Step one is to check all new commands that a session has received. This will process the commands and/or
            # add actions to the Action Queue as needed. It will also handle disconnects and other events that the
            # game loop needs to know about.
            await sess_srv.update_loop(self, delta)

            # if not enough time has passed since the last update loop, we'll delay calling it just slightly.
            remaining = interval - delta
            if remaining > 0:
                await asyncio.sleep(remaining.total_seconds())
            self.world.process()
            current_timestamp = utcnow()
