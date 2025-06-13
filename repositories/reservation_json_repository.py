import os

from json_services import JSONServices
from models.reservation import Reservation


class ReservationJsonRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._reservations = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("reservations", [])
        return [Reservation.deserialize(reservation) for reservation in data]

    def all(self):
        return self._reservations

    def add(self, reservation: Reservation):
        self._reservations.append(reservation)

    def save(self):
        serialized_data = [reservation.serialize() for reservation in self._reservations]
        JSONServices.save(self.file_path, {"reservations": serialized_data})
