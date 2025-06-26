import os

from entities.reservation import Reservation
from json_services import JSONServices
from repository_protocols.reservation_repository import ReservationRepository


class ReservationJsonRepository(ReservationRepository):
    """Repository for managing reservations stored in a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._reservations: list[Reservation] = self._load()

    def _load(self) -> list[Reservation]:
        """Load reservations from the JSON file. If the file does not exist, return an empty list."""
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("reservations", [])
        return [Reservation.deserialize(reservation) for reservation in data]

    def reload(self) -> None:
        """Reload the reservations from the JSON file."""
        self._reservations = self._load()

    def _add(self, reservation: Reservation) -> None:
        """Add a reservation to the repository."""
        self._reservations.append(reservation)

    def all(self) -> list[Reservation]:
        """Get all reservations from the repository."""
        return self._reservations

    def get_club_reservations_for_competition(self, club_id: str, competition_id: str) -> list[Reservation]:
        """Get all reservations for a specific club and competition."""
        return [
            reservation
            for reservation in self._reservations
            if reservation.club_id == club_id and reservation.competition_id == competition_id
        ]

    def get_total_places_club_reservation_for_competition(self, club_id: str, competition_id: str) -> int:
        """Get the total number of places reserved by a club for a specific competition."""
        reservations = self.get_club_reservations_for_competition(club_id, competition_id)
        return sum(reservation.reserved_places for reservation in reservations)

    def save(self, reservation: Reservation) -> None:
        """Save a new reservation to the repository."""
        self._add(reservation)
        serialized_data = [reservation.serialize() for reservation in self._reservations]
        JSONServices.save(self.file_path, {"reservations": serialized_data})
