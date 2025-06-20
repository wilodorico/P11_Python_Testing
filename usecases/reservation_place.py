from models.reservation import Reservation
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

    def execute(self, club_name: str, competition_name: str, places: int, date: str) -> Reservation:
        club = self._club_repository.find_by_name(club_name)

        if not club:
            raise ValueError(f"Club '{club_name}' not found.")

        competition = self._competition_repository.find_by_name(competition_name)

        if not competition:
            raise ValueError(f"Competition '{competition_name}' not found.")

        if places <= 0:
            raise ValueError("Number of places must be greater than zero.")

        if not club.has_enough_points(places):
            raise ValueError("Club does not have enough points to reserve places.")

        if not competition.is_within_reservation_limit(places):
            raise ValueError(f"Maximum booking limit is {competition.max_places_per_reservation} places.")

        if not competition.can_reserve(places):
            raise ValueError("Not enough available places in the competition.")

        reservation = club.reserve(competition, places, date)

        self._reservation_repository.add(reservation)
        self._reservation_repository.save()
        self._club_repository.save()
        self._competition_repository.save()

        return reservation
