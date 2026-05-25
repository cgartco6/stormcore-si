from pathlib import Path


class RepairEngine:
    async def repair(self, repo_path: str):
        for folder in Path(repo_path).rglob("*"):
            if folder.is_dir():
                init_file = folder / "__init__.py"

                if not init_file.exists():
                    init_file.write_text("")
