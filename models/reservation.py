import uuid


class Reservation:
    def __init__(self, club_id: str, competition_id: str, reserved_places: int, date: str):
        self._id = uuid.uuid4()
        self._club_id = club_id
        self._competition_id = competition_id
        self._reserved_places = reserved_places
        self._date = date

    def __str__(self) -> str:
        return (
            f"Reservation(id={self._id}, club_id={self._club_id}, "
            f"competition_id={self._competition_id}, reserved_places={self._reserved_places}, date={self._date})"
        )
