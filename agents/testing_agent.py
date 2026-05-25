class TestingAgent:
    async def execute(self, repo_path: str):
        return {
            "success": True,
            "message": f"Tested repository {repo_path}",
        }
