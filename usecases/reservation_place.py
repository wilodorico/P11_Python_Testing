from datetime import datetime

from repository_protocols.club_repository import ClubRepository
from repository_protocols.competition_repository import CompetitionRepository
from repository_protocols.reservation_repository import ReservationRepository


class ReservePlaceUseCase:
    def __init__(
        self,
        club_repository: ClubRepository,
        competition_repository: CompetitionRepository,
        reservation_repository: ReservationRepository,
    ):
        self._club_repository = club_repository
        self._competition_repository = competition_repository
        self._reservation_repository = reservation_repository

    def execute(self, club_name: str, competition_name: str, places: int, date: datetime) -> None:
        club = self._club_repository.find_by_name(club_name)

        if not club:
            raise ValueError("Club not found.")

        competition = self._competition_repository.find_by_name(competition_name)

        if not competition:
            raise ValueError("Competition not found.")

        if places <= 0:
            raise ValueError("Number of places must be greater than zero.")

        if not club.has_enough_points(places):
            raise ValueError("Club does not have enough points to reserve places.")

        if not competition.is_within_reservation_limit(places):
            raise ValueError(f"Maximum booking limit is {competition.max_places_per_reservation} places.")

        if not competition.can_reserve(places):
            raise ValueError("Not enough available places in the competition.")

        if competition.date < date:
            raise ValueError("Cannot reserve places for a past competition.")

        reservation = club.reserve(competition, places, date)

        self._reservation_repository.save(reservation)
        self._club_repository.update(club)
        self._competition_repository.update(competition)
        self._competition_repository.update(competition)
