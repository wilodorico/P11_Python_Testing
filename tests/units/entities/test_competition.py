import pytest

from entities.club import Club
from entities.competition import Competition


@pytest.fixture
def club():
    return Club(name="Test Club", email="test@club.com", points=10)


@pytest.fixture
def competition():
    return Competition(name="Test Competition", date="2025-10-01", available_places=5)


class TestCompetition:
    def test_can_reserve(self, competition):
        assert competition.can_reserve(3) is True

    def test_cannot_reserve(self, competition):
        assert competition.can_reserve(6) is False

    def test_is_within_reservation_limit(self, competition):
        assert competition.is_within_reservation_limit(3, 5) is True

    def test_exceeds_reservation_limit(self, competition):
        assert competition.is_within_reservation_limit(5, 8) is False

    def test_reserve_places_raises_error_if_not_enough_available_places(self, club, competition):
        with pytest.raises(ValueError, match="Not enough available places to reserve."):
            competition.reserve_places(club, places=6, date=None)

    def test_reserve_places_raises_error_if_club_not_enough_points(self, club, competition):
        club.consume_points(10)
        with pytest.raises(ValueError, match="Not enough points to reserve places."):
            competition.reserve_places(club, places=5, date=None)
