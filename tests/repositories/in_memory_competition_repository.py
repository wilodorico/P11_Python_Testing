from models.competition import Competition
from repository_protocols.competition_repository import CompetitionRepository


class InMemoryCompetitionRepository(CompetitionRepository):
    def __init__(self, competitions: list[Competition]):
        self._competitions = competitions

    def all(self) -> list[Competition]:
        return self._competitions

    def find_by_name(self, name: str) -> Competition | None:
        return next((comp for comp in self._competitions if comp.name == name), None)

    def update(self, competition: Competition) -> None:
        for i, existing_competition in enumerate(self._competitions):
            if existing_competition.name == competition.name:
                self._competitions[i] = competition
                break
        else:
            self._competitions.append(competition)
