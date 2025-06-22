from models.club import Club
from repository_protocols.club_repository import ClubRepository


class InMemoryClubRepository(ClubRepository):
    def __init__(self, clubs: list[Club]):
        self._clubs = clubs

    def all(self) -> list[Club]:
        return self._clubs

    def find_by_name(self, name: str) -> Club | None:
        return next((club for club in self._clubs if club.name == name), None)

    def find_by_email(self, email: str) -> Club | None:
        return next((club for club in self._clubs if club.email == email), None)

    def update(self, club: Club) -> None:
        for i, existing_club in enumerate(self._clubs):
            if existing_club.name == club.name:
                self._clubs[i] = club
                break
        else:
            self._clubs.append(club)
