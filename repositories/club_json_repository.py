import os

from json_services import JSONServices
from models.club import Club


class ClubJsonRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self._clubs = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("clubs", [])
        return [Club.deserialize(club) for club in data]

    def all(self):
        return self._clubs

    def find_by_name(self, name: str):
        return next((club for club in self._clubs if club.name == name), None)

    def save(self):
        serialized_data = [club.serialize() for club in self._clubs]
        JSONServices.save(self.file_path, {"clubs": serialized_data})
