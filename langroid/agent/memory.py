import json
import os
from typing import List, Dict, Any

class LongTermMemory:
    """
    Persistent memory layer for Langroid agents.
    Supports local file storage and is ready for Redis integration.
    """
    def __init__(self, storage_path: str = "/home/ubuntu/SSPPTTSPT/storage/memory"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def save_context(self, agent_id: str, context: List[Dict[str, Any]]):
        file_path = os.path.join(self.storage_path, f"{agent_id}.json")
        with open(file_path, 'w') as f:
            json.dump(context, f)

    def load_context(self, agent_id: str) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.storage_path, f"{agent_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []

    def clear_memory(self, agent_id: str):
        file_path = os.path.join(self.storage_path, f"{agent_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
