class CoderAgent:
    async def execute(self, repo_path: str):
        return {
            "success": True,
            "message": f"Generated improvements for {repo_path}",
        }
