from models.club import Club
from repository_protocols.club_repository import ClubRepository


class InMemoryClubRepository(ClubRepository):
    def __init__(self):
        self._clubs: list[Club] = []

    def all(self) -> list[Club]:
        return self._clubs

    def find_by_name(self, name: str) -> Club | None:
        return next((club for club in self._clubs if club.name == name), None)

    def find_by_email(self, email: str) -> Club | None:
        return next((club for club in self._clubs if club.email == email), None)

    def save(self) -> None:
        # In-memory repository does not need to save to a file
        pass
