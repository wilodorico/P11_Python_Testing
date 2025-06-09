import uuid


class Club:
    def __init__(self, name: str, email: str, points: int):
        self._id = uuid.uuid4()
        self._name = name
        self._email = email
        self._points = points

    def has_enough_points(self, points: int) -> bool:
        """Check if the club has enough points."""
        return self._points >= points

    def __str__(self) -> str:
        return f"Club(id={self._id}, name={self._name}, email={self._email}, points={self._points})"
