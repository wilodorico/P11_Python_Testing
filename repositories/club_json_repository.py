import os

from entities.club import Club
from json_services import JSONServices
from ports.club_repository import ClubRepository


class ClubJsonRepository(ClubRepository):
    """Repository for managing clubs stored in a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._clubs: list[Club] = self._load()

    def _load(self) -> list[Club]:
        """Load clubs from the JSON file. If the file does not exist, return an empty list."""
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("clubs", [])
        return [Club.deserialize(club) for club in data]

    def reload(self) -> None:
        """Reload the clubs from the JSON file."""
        self._clubs = self._load()

    def all(self) -> list[Club]:
        """Get all clubs from the repository."""
        return self._clubs

    def find_by_name(self, name: str) -> Club | None:
        """Find a club by its name."""
        return next((club for club in self._clubs if club.name == name), None)

    def find_by_email(self, email: str) -> Club | None:
        """Find a club by its email."""
        return next((club for club in self._clubs if club.email == email), None)

    def update(self, club: Club) -> None:
        """Update an existing club in the repository."""
        for i, existing_club in enumerate(self._clubs):
            if existing_club.name == club.name:
                self._clubs[i] = club
                break
        serialized_data = [club.serialize() for club in self._clubs]
        JSONServices.save(self.file_path, {"clubs": serialized_data})
