from enum import Enum
import json

class Status(str, Enum):
    RUNNING = "running"
    PREPARING = "preparing"
    FAILED = "failed"
    DONE = "done"

class StatusEntity:
    def __init__(self, state):
        # Check if the provided state is a valid status
        if state not in Status.__members__.values():
            raise ValueError(f"Invalid status: {state}")
        self.state = state

    def to_dict(self):
        return {"state": self.state}

    @classmethod
    def from_dict(cls, data):
        return cls(state=data["state"])