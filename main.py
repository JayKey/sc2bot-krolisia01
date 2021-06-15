import sc2

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON

class Krolisia01Bot(sc2.BotAI):
    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_workers()

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford() and self.can_feed() and self.need_more_workers():
                await self.do(nexus.train(PROBE))

    async def need_more_workers(self):
        if self.units(NEXUS).ready.count() * 24 < self.units(PROBE).ready.count():
            return 1

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)

run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, Krolisia01Bot()),
    Computer(Race.Zerg, Difficulty.Easy)
], realtime=True)

