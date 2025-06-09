import uuid


class Club:
    def __init__(self, name: str, email: str, points: int):
        self._id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._points = points

    def has_enough_points(self, points: int) -> bool:
        """Check if the club has enough points."""
        return self._points >= points

    @property
    def name(self) -> str:
        """Get the name of the club."""
        return self._name

    @classmethod
    def deserialize(cls, data: dict):
        """Deserialize data into the Club object."""
        club = cls(
            name=data.get("name"),
            email=data.get("email"),
            points=int(data.get("points")),
        )
        club._id = data.get("id")
        return club

    def serialize(self) -> dict:
        """Serialize the Club object into a dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "points": str(self._points),
        }

    def __str__(self) -> str:
        return f"Club(id={self._id}, name={self._name}, email={self._email}, points={self._points})"
