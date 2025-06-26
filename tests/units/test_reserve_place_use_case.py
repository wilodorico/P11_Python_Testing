import datetime

import pytest

from models.club import Club
from models.competition import Competition
from models.reservation import Reservation
from tests.repositories.in_memory_club_repository import InMemoryClubRepository
from tests.repositories.in_memory_competition_repository import InMemoryCompetitionRepository
from tests.repositories.in_memory_reservation_repository import InMemoryReservationRepository
from usecases.reservation_place import ReservePlaceUseCase


@pytest.fixture
def club():
    return Club(name="Test Club", email="test@club.com", points=20)


@pytest.fixture
def future_competition():
    future_date = datetime.datetime.now() + datetime.timedelta(days=15)
    return Competition(name="Test Competition", date=future_date, available_places=20)


@pytest.fixture
def date_now():
    return datetime.datetime.now()


def test_successful_reserve_place(club, future_competition, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )
    use_case.execute(club_name="Test Club", competition_name="Test Competition", places=5, date=date_now)

    assert club.points == 15
    assert future_competition.available_places == 15
    assert len(reservation_repo.all()) == 1
    reservation = reservation_repo.all()[0]
    assert reservation.club_id == club.id
    assert reservation.competition_id == future_competition.id
    assert reservation.reserved_places == 5
    assert reservation.date == date_now
    assert reservation.date == date_now


def test_reserve_place_with_past_competition_raises_error(club, date_now):
    past_date = datetime.datetime.now() - datetime.timedelta(days=15)
    past_competition = Competition(name="Past Competition", date=past_date, available_places=20)

    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([past_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Cannot reserve places for a past competition."):
        use_case.execute(club_name="Test Club", competition_name="Past Competition", places=5, date=date_now)


def test_reserve_place_with_club_not_found_raises_error(future_competition, date_now):
    club_repo = InMemoryClubRepository([])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Club not found."):
        use_case.execute(club_name="Unknown Club", competition_name="Test Competition", places=5, date=date_now)


def test_reserve_place_with_competition_not_found_raises_error(club, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Competition not found."):
        use_case.execute(club_name="Test Club", competition_name="Unknown Competition", places=5, date=date_now)


def test_reserve_place_with_zero_places_raises_error(club, future_competition, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Number of places must be greater than zero."):
        use_case.execute(club_name="Test Club", competition_name="Test Competition", places=0, date=date_now)


def test_reserve_place_with_negative_places_raises_error(club, future_competition, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Number of places must be greater than zero."):
        use_case.execute(club_name="Test Club", competition_name="Test Competition", places=-5, date=date_now)


def test_reserve_place_with_insufficient_points_raises_error(club, future_competition, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Club does not have enough points to reserve places."):
        use_case.execute(club_name="Test Club", competition_name="Test Competition", places=25, date=date_now)


def test_reserve_place_with_exceeding_max_places_per_reservation_raises_error(club, future_competition, date_now):
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([future_competition])
    reservation_repo = InMemoryReservationRepository()

    reserved_places = 8
    remaining_quota = future_competition.MAX_PLACES_PER_RESERVATION - reserved_places

    existing_reservations = Reservation(
        club_id=club.id, competition_id=future_competition.id, reserved_places=reserved_places, date=date_now
    )

    reservation_repo.save(existing_reservations)

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(
        ValueError,
        match=f"You have already reserved {reserved_places} place\\(s\\).*You can only reserve {remaining_quota} more.",
    ):
        use_case.execute(
            club_name="Test Club",
            competition_name="Test Competition",
            places=5,
            date=date_now,
        )


def test_reserve_place_with_not_enough_available_places_raises_error(club, date_now):
    future_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
    competition = Competition(name="Test Competition", date=future_date, available_places=10)
    club_repo = InMemoryClubRepository([club])
    competition_repo = InMemoryCompetitionRepository([competition])
    reservation_repo = InMemoryReservationRepository()

    use_case = ReservePlaceUseCase(
        club_repository=club_repo, competition_repository=competition_repo, reservation_repository=reservation_repo
    )

    with pytest.raises(ValueError, match="Not enough available places in the competition."):
        use_case.execute(club_name="Test Club", competition_name="Test Competition", places=11, date=date_now)
