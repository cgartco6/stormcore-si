from agents.coder_agent import CoderAgent
from agents.reviewer_agent import ReviewerAgent
from agents.testing_agent import TestingAgent
from agents.repair_agent import RepairAgent


class SwarmOrchestrator:
    def initialize(self):
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.testing = TestingAgent()
        self.repair = RepairAgent()

    async def execute(self, repo_path: str):
        code = await self.coder.execute(repo_path)
        review = await self.reviewer.execute(repo_path)
        tests = await self.testing.execute(repo_path)

        if not tests["success"]:
            await self.repair.execute(repo_path)

        return {
            "coder": code,
            "reviewer": review,
            "testing": tests,
        }
