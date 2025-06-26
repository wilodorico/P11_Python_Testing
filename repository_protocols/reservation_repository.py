from typing import Protocol

from entities.reservation import Reservation


class ReservationRepository(Protocol):
    """Protocol for a repository that manages Reservation entities."""

    def all(self) -> list[Reservation]: ...

    def get_club_reservations_for_competition(self, club_id: str, competition_id: str) -> list[Reservation]: ...

    def get_total_places_club_reservation_for_competition(self, club_id: str, competition_id: str) -> int: ...

    def save(self, reservation: Reservation) -> None: ...
