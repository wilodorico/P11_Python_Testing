from typing import Protocol

from models.competition import Competition


class CompetitionRepository(Protocol):
    def all(self) -> list[Competition]: ...

    def find_by_name(self, name: str) -> Competition | None: ...

    def update(self, competition: Competition) -> None: ...
