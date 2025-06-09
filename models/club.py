import uuid


class Club:
    def __init__(self, name: str, email: str, points: int):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.points = points

    def __str__(self) -> str:
        return f"Club(id={self.id}, name={self.name}, email={self.email}, points={self.points})"
