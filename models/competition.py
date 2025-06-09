import uuid


class Competition:
    def __init__(self, name: str, date: str, available_places: int):
        self._id = uuid.uuid4()
        self._name = name
        self._date = date
        self._available_places = available_places

    def can_reserve(self, places: int) -> bool:
        """Check if there are enough available places to reserve."""
        return self._available_places >= places

    def __str__(self) -> str:
        return f"Competition(id={self._id}, name={self._name}, date={self._date}, available_places={self._available_places})"
