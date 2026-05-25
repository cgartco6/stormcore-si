import json
from pathlib import Path


class MemoryManager:
    def __init__(self):
        self.base = Path("memory")

    def initialize(self):
        self.base.mkdir(exist_ok=True)

    def remember(self, key, value):
        with open(self.base / f"{key}.json", "w") as file:
            json.dump(value, file, indent=2)
