import uuid


class Reservation:
    def __init__(self, club_id: str, competition_id: str, reserved_places: int, date: str):
        self.id = uuid.uuid4()
        self.club_id = club_id
        self.competition_id = competition_id
        self.reserved_places = reserved_places
        self.date = date

    def __str__(self) -> str:
        return (
            f"Reservation(id={self.id}, club_id={self.club_id}, "
            f"competition_id={self.competition_id}, reserved_places={self.reserved_places}, date={self.date})"
        )
