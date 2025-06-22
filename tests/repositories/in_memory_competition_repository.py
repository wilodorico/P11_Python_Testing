from models.competition import Competition
from repository_protocols.competition_repository import CompetitionRepository


class InMemoryCompetitionRepository(CompetitionRepository):
    def __init__(self):
        self._competitions: list[Competition] = []

    def all(self) -> list[Competition]:
        return self._competitions

    def find_by_name(self, name: str) -> Competition | None:
        return next((comp for comp in self._competitions if comp.name == name), None)

    def save(self) -> None:
        # In-memory repository does not need to save to a file
        pass
