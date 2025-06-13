import os

from json_services import JSONServices
from models.competition import Competition


class CompetitionJsonRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self._competitions = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("competitions", [])
        return [Competition.deserialize(competition) for competition in data]

    def all(self):
        return self._competitions

    def find_by_name(self, name: str):
        return next((competition for competition in self._competitions if competition.name == name), None)

    def save(self):
        serialized_data = [competition.serialize() for competition in self._competitions]
        JSONServices.save(self.file_path, {"competitions": serialized_data})
