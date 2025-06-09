import pytest

from models.club import Club


@pytest.fixture
def club():
    return Club(name="Test Club", email="test@example.com", points=10)


class TestClub:
    def test_has_enough_points(self, club):
        assert club.has_enough_points(5) is True

    def test_has_not_enough_points(self, club):
        assert club.has_enough_points(11) is False
