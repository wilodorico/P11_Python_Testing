from typing import Protocol

from entities.competition import Competition


class CompetitionRepository(Protocol):
    """Protocol for a repository that manages Competition entities."""

    def all(self) -> list[Competition]: ...

    def find_by_name(self, name: str) -> Competition | None: ...

    def update(self, competition: Competition) -> None: ...
