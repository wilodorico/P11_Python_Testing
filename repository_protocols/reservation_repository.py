from typing import Protocol

from models.reservation import Reservation


class ReservationRepository(Protocol):
    def all(self) -> list[Reservation]: ...

    def save(self, reservation: Reservation) -> None: ...
