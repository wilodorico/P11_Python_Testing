import uuid

from models.reservation import Reservation


class Competition:
    MAX_PLACES_PER_RESERVATION = 12

    def __init__(
        self, name: str, date: str, available_places: int, max_places_per_reservation: int = MAX_PLACES_PER_RESERVATION
    ):
        self._id = str(uuid.uuid4())
        self._name = name
        self._date = date
        self._available_places = available_places
        self._max_places_per_reservation = max_places_per_reservation

    def can_reserve(self, places: int) -> bool:
        """Check if there are enough available places to reserve."""
        return self._available_places >= places

    def is_within_reservation_limit(self, places: int) -> bool:
        """Check if the reservation does not exceed the maximum places per reservation."""
        return places <= self._max_places_per_reservation

    def reserve_places(self, club, places, date):
        if not self.can_reserve(places):
            raise ValueError("Not enough available places to reserve.")
        if not club.has_enough_points(places):
            raise ValueError("Not enough points to reserve places.")

        club.consume_points(places)
        self._available_places -= places

        return Reservation(club.id, self._id, places, date)

    @property
    def id(self) -> str:
        """Get the ID of the competition."""
        return self._id

    @property
    def name(self) -> str:
        """Get the name of the competition."""
        return self._name

    @property
    def available_places(self) -> int:
        """Get the number of available places."""
        return self._available_places

    @property
    def max_places_per_reservation(self) -> int:
        """Get the maximum places per reservation."""
        return self._max_places_per_reservation

    @classmethod
    def deserialize(cls, data: dict):
        """Deserialize data into the Competition object."""
        competition = cls(
            name=data.get("name"),
            date=data.get("date"),
            available_places=int(data.get("available_places")),
        )
        competition._id = data.get("id")
        return competition

    def serialize(self) -> dict:
        """Serialize the Competition object into a dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "date": self._date,
            "available_places": str(self._available_places),
        }

    def __str__(self) -> str:
        return f"Competition(id={self._id}, name={self._name}, date={self._date}, available_places={self._available_places})"
