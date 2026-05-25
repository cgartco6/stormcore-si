class ObjectiveGuardian:
    def initialize(self):
        self.primary_objective = "COMPLETE_REPOSITORIES"

    async def validate(self, repo_path: str):
        return True
