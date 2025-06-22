import os

from json_services import JSONServices
from models.reservation import Reservation
from repository_protocols.reservation_repository import ReservationRepository


class ReservationJsonRepository(ReservationRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._reservations: list[Reservation] = self._load()

    def _load(self) -> list[Reservation]:
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("reservations", [])
        return [Reservation.deserialize(reservation) for reservation in data]

    def _add(self, reservation: Reservation) -> None:
        self._reservations.append(reservation)

    def all(self) -> list[Reservation]:
        return self._reservations

    def save(self, reservation: Reservation) -> None:
        self._add(reservation)
        serialized_data = [reservation.serialize() for reservation in self._reservations]
        JSONServices.save(self.file_path, {"reservations": serialized_data})
