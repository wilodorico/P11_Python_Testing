import uuid


class Reservation:
    def __init__(self, club_id: str, competition_id: str, reserved_places: int, date: str):
        self._id = str(uuid.uuid4())
        self._club_id = club_id
        self._competition_id = competition_id
        self._reserved_places = reserved_places
        self._date = date

    @classmethod
    def deserialize(cls, data: dict):
        """Deserialize data into the Reservation object."""
        reservation = cls(
            club_id=data.get("club_id"),
            competition_id=data.get("competition_id"),
            reserved_places=int(data.get("reserved_places")),
            date=data.get("date"),
        )
        reservation._id = data.get("id")
        return reservation

    def serialize(self) -> dict:
        """Serialize the Reservation object into a dictionary."""
        return {
            "id": self._id,
            "club_id": self._club_id,
            "competition_id": self._competition_id,
            "reserved_places": str(self._reserved_places),
            "date": self._date,
        }

    def __str__(self) -> str:
        return (
            f"Reservation(id={self._id}, club_id={self._club_id}, "
            f"competition_id={self._competition_id}, reserved_places={self._reserved_places}, date={self._date})"
        )
