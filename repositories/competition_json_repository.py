import os

from json_services import JSONServices
from models.competition import Competition
from repository_protocols.competition_repository import CompetitionRepository


class CompetitionJsonRepository(CompetitionRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._competitions: list[Competition] = self._load()

    def _load(self) -> list[Competition]:
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("competitions", [])
        return [Competition.deserialize(competition) for competition in data]

    def reload(self) -> None:
        """Reload the competitions from the JSON file."""
        self._competitions = self._load()

    def all(self) -> list[Competition]:
        return self._competitions

    def find_by_name(self, name: str) -> Competition | None:
        return next((competition for competition in self._competitions if competition.name == name), None)

    def save(self) -> None:
        serialized_data = [competition.serialize() for competition in self._competitions]
        JSONServices.save(self.file_path, {"competitions": serialized_data})
