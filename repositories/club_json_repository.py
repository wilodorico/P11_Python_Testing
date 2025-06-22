import os

from json_services import JSONServices
from models.club import Club
from repository_protocols.club_repository import ClubRepository


class ClubJsonRepository(ClubRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._clubs: list[Club] = self._load()

    def _load(self) -> list[Club]:
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("clubs", [])
        return [Club.deserialize(club) for club in data]

    def reload(self) -> None:
        """Reload the clubs from the JSON file."""
        self._clubs = self._load()

    def all(self) -> list[Club]:
        return self._clubs

    def find_by_name(self, name: str) -> Club | None:
        return next((club for club in self._clubs if club.name == name), None)

    def find_by_email(self, email: str) -> Club | None:
        return next((club for club in self._clubs if club.email == email), None)

    def update(self, club: Club) -> None:
        for i, existing_club in enumerate(self._clubs):
            if existing_club.name == club.name:
                self._clubs[i] = club
                break
        serialized_data = [club.serialize() for club in self._clubs]
        JSONServices.save(self.file_path, {"clubs": serialized_data})
