class StatusEntity:
    def __init__(self, state):
        self.state = state

    def to_dict(self):
        return {"state": self.state}

    @classmethod
    def from_dict(cls, data):
        return cls(state=data["state"])