from typing import Protocol

from models.reservation import Reservation


class ReservationRepository(Protocol):
    def all(self) -> list[Reservation]: ...

    def add(self, reservation: Reservation) -> None: ...

    def save(self) -> None: ...
