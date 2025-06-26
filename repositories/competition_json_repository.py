import os

from entities.competition import Competition
from json_services import JSONServices
from repository_protocols.competition_repository import CompetitionRepository


class CompetitionJsonRepository(CompetitionRepository):
    """Repository for managing competitions stored in a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._competitions: list[Competition] = self._load()

    def _load(self) -> list[Competition]:
        """Load competitions from the JSON file. If the file does not exist, return an empty list."""
        if not os.path.exists(self.file_path):
            return []

        data = JSONServices.load(self.file_path).get("competitions", [])
        return [Competition.deserialize(competition) for competition in data]

    def reload(self) -> None:
        """Reload the competitions from the JSON file."""
        self._competitions = self._load()

    def all(self) -> list[Competition]:
        """Get all competitions from the repository."""
        return self._competitions

    def find_by_name(self, name: str) -> Competition | None:
        """Find a competition by its name."""
        return next((competition for competition in self._competitions if competition.name == name), None)

    def update(self, competition: Competition) -> None:
        """Update an existing competition in the repository."""
        for i, existing_competition in enumerate(self._competitions):
            if existing_competition.name == competition.name:
                self._competitions[i] = competition
                break
        serialized_data = [competition.serialize() for competition in self._competitions]
        JSONServices.save(self.file_path, {"competitions": serialized_data})
