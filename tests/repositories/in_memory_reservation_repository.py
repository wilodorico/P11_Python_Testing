from models.reservation import Reservation
from repository_protocols.reservation_repository import ReservationRepository


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self._reservations: list[Reservation] = []

    def all(self) -> list[Reservation]:
        return self._reservations

    def get_club_reservations_for_competition(self, club_id: str, competition_id: str) -> list[Reservation]:
        return [
            reservation
            for reservation in self._reservations
            if reservation.club_id == club_id and reservation.competition_id == competition_id
        ]

    def get_total_places_club_reservation_for_competition(self, club_id: str, competition_id: str) -> int:
        reservations = self.get_club_reservations_for_competition(club_id, competition_id)
        return sum(reservation.reserved_places for reservation in reservations)

    def save(self, reservation: Reservation) -> None:
        self._reservations.append(reservation)
