import subprocess


class ValidationPipeline:
    async def validate(self, repo_path: str):
        checks = {
            "ruff": self.run(["ruff", "check", repo_path]),
            "mypy": self.run(["mypy", repo_path]),
            "bandit": self.run(["bandit", "-r", repo_path]),
        }

        success = all(item["success"] for item in checks.values())

        return {
            "success": success,
            "checks": checks,
        }

    def run(self, command):
        result = subprocess.run(command, capture_output=True, text=True)

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
