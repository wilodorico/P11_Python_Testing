import pytest

from models.competition import Competition


@pytest.fixture
def competition():
    return Competition(name="Test Competition", date="2023-10-01", available_places=5)


class TestCompetition:
    def test_can_reserve(self, competition):
        assert competition.can_reserve(3) is True

    def test_cannot_reserve(self, competition):
        assert competition.can_reserve(6) is False

    def test_is_within_reservation_limit(self, competition):
        assert competition.is_within_reservation_limit(10) is True

    def test_exceeds_reservation_limit(self, competition):
        assert competition.is_within_reservation_limit(13) is False
