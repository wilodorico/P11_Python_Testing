import uuid
from datetime import datetime

from entities.club import Club
from entities.reservation import Reservation


class Competition:
    """Class representing a competition with a name, date, available places and maximum places per reservation."""

    MAX_PLACES_PER_RESERVATION = 12

    def __init__(
        self,
        name: str,
        date: datetime,
        available_places: int,
        max_places_per_reservation: int = MAX_PLACES_PER_RESERVATION,
    ):
        self._id = str(uuid.uuid4())
        self._name = name
        self._date = date
        self._available_places = available_places
        self._max_places_per_reservation = max_places_per_reservation

    def _deduct_available_places(self, places: int) -> None:
        self._available_places -= places

    def can_reserve(self, places: int) -> bool:
        """Check if there are enough available places to reserve."""
        return self._available_places >= places

    def is_within_reservation_limit(self, places: int, total_already_reserved: int) -> bool:
        """Check if the total reserved places stay within the allowed limit."""
        return total_already_reserved + places <= self._max_places_per_reservation

    def reserve_places(self, club: Club, places: int, date: datetime, total_already_reserved: int = 0) -> Reservation:
        """Reserve places for a club in the competition."""
        if date is None:
            raise ValueError("Reservation date is required.")

        if places <= 0:
            raise ValueError("Number of places must be greater than zero.")

        if self.date < date:
            raise ValueError("Cannot reserve places for a past competition.")

        if not club.has_enough_points(places):
            raise ValueError("Club does not have enough points to reserve places.")

        if not self.is_within_reservation_limit(places, total_already_reserved):
            remaining_quota = self._max_places_per_reservation - total_already_reserved
            raise ValueError(
                f"You have already reserved {total_already_reserved} place(s). "
                f"You can only reserve {remaining_quota} more."
            )

        if not self.can_reserve(places):
            raise ValueError("Not enough available places in the competition.")

        club.consume_points(places)
        self._deduct_available_places(places)

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
    def date(self) -> datetime:
        """Get the date of the competition."""
        return self._date

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
            date=datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S"),
            available_places=int(data.get("available_places")),
        )
        competition._id = data.get("id")
        return competition

    def serialize(self) -> dict:
        """Serialize the Competition object into a dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "date": self._date.strftime("%Y-%m-%d %H:%M:%S"),
            "available_places": str(self._available_places),
        }

    def __str__(self) -> str:
        return (
            f"Competition(id={self._id}, name={self._name}, "
            f"date={self._date}, available_places={self._available_places})"
        )
