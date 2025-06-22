from models.reservation import Reservation
from repository_protocols.reservation_repository import ReservationRepository


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self._reservations: list[Reservation] = []

    def all(self) -> list[Reservation]:
        return self._reservations

    def save(self, reservation: Reservation) -> None:
        self._reservations.append(reservation)
