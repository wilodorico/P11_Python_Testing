import datetime

import pytest

from models.club import Club
from models.competition import Competition
from tests.repositories.in_memory_club_repository import InMemoryClubRepository
from tests.repositories.in_memory_competition_repository import InMemoryCompetitionRepository
from tests.repositories.in_memory_reservation_repository import InMemoryReservationRepository
from usecases.reservation_place import ReservePlaceUseCase


def test_successful_reserve_place():
    club = Club(name="Test Club", email="test@club.com", points=20)
    competition = Competition(name="Test Competition", date="2023-10-01 10:00:00", available_places=20)

    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    use_case.execute(club_name="Test Club", competition_name="Test Competition", places=5, date=date_now)

    assert club.points == 15
    assert competition.available_places == 15
    assert len(reservation_repo.all()) == 1
    reservation = reservation_repo.all()[0]
    assert reservation.club_id == club.id
    assert reservation.competition_id == competition.id
    assert reservation.reserved_places == 5
    assert reservation.date == date_now
    assert reservation.date == date_now


def test_reserve_place_with_club_not_found_raises_error():
    competition = Competition(name="Test Competition", date="2023-10-01 10:00:00", available_places=20)
    club_repo = InMemoryClubRepository([])
    competition_repo = InMemoryCompetitionRepository([competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with pytest.raises(ValueError, match="Club not found."):
        use_case.execute(club_name="Unknown Club", competition_name="Test Competition", places=5, date=date_now)


def test_reserve_place_with_competition_not_found_raises_error():
    club = Club(name="Test Club", email="test@club.com", points=20)
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with pytest.raises(ValueError, match="Competition not found."):
        use_case.execute(club_name="Test Club", competition_name="Unknown Competition", places=5, date=date_now)
