from loguru import logger
from core.swarm.orchestrator import SwarmOrchestrator
from core.verification.validator import ValidationPipeline
from core.repair.repair_engine import RepairEngine
from core.memory.memory_manager import MemoryManager
from core.objectives.guardian import ObjectiveGuardian


class StormCoreEngine:
    def __init__(self):
        self.memory = MemoryManager()
        self.guardian = ObjectiveGuardian()
        self.swarm = SwarmOrchestrator()
        self.validator = ValidationPipeline()
        self.repair = RepairEngine()

    def boot(self):
        logger.info("StormCore Booting")
        self.memory.initialize()
        self.guardian.initialize()
        self.swarm.initialize()
        logger.success("StormCore Ready")

    async def complete_repository(self, repo_path: str):
        await self.guardian.validate(repo_path)

        swarm_result = await self.swarm.execute(repo_path)

        validation = await self.validator.validate(repo_path)

        if not validation["success"]:
            await self.repair.repair(repo_path)

        self.memory.remember(
            "last_repository",
            {
                "repo": repo_path,
                "status": validation,
            },
        )

        return {
            "swarm": swarm_result,
            "validation": validation,
        }
