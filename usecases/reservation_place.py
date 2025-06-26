from datetime import datetime

from repository_protocols.club_repository import ClubRepository
from repository_protocols.competition_repository import CompetitionRepository
from repository_protocols.reservation_repository import ReservationRepository


class ReservePlaceUseCase:
    """Use case for reserving places in a competition for a club."""

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
        """Reserves places in a competition for a club."""
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

        total_already_reserved = self._reservation_repository.get_total_places_club_reservation_for_competition(
            club.id, competition.id
        )
        if not competition.is_within_reservation_limit(places, total_already_reserved):
            remaining_quota = competition.max_places_per_reservation - total_already_reserved
            raise ValueError(
                f"You have already reserved {total_already_reserved} place(s). "
                f"You can only reserve {remaining_quota} more."
            )

        if not competition.can_reserve(places):
            raise ValueError("Not enough available places in the competition.")

        if competition.date < date:
            raise ValueError("Cannot reserve places for a past competition.")

        reservation = club.reserve(competition, places, date)

        self._reservation_repository.save(reservation)
        self._club_repository.update(club)
        self._competition_repository.update(competition)
