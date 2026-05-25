class ReviewerAgent:
    async def execute(self, repo_path: str):
        return {
            "success": True,
            "message": f"Reviewed repository {repo_path}",
        }
