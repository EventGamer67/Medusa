class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}')"

    def to_json(self):
        return f"{self.id}${self.name}"