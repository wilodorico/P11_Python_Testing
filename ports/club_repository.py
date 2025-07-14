from typing import Protocol

from entities.club import Club


class ClubRepository(Protocol):
    """Protocol for a repository that manages Club entities."""

    def all(self) -> list[Club]: ...

    def find_by_name(self, name: str) -> Club | None: ...

    def find_by_email(self, email: str) -> Club | None: ...

    def update(self, club: Club) -> None: ...
