import os

from entities.reservation import Reservation
from json_services import JSONServices
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

    def reload(self) -> None:
        self._reservations = self._load()

    def _add(self, reservation: Reservation) -> None:
        self._reservations.append(reservation)

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
        self._add(reservation)
        serialized_data = [reservation.serialize() for reservation in self._reservations]
        JSONServices.save(self.file_path, {"reservations": serialized_data})
