import pytest

from entities.club import Club


@pytest.fixture
def club():
    return Club(name="Test Club", email="test@example.com", points=10)


class TestClub:
    def test_has_enough_points(self, club):
        assert club.has_enough_points(5) is True

    def test_consume_points_raises_error_if_not_enough_points(self, club):
        with pytest.raises(ValueError, match="Not enough points to consume."):
            club.consume_points(15)

    def test_consume_points_deducts_points_if_enough(self, club):
        club.consume_points(5)
        assert club._points == 5
