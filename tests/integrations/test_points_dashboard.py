from adapters.in_memory_club_repository import InMemoryClubRepository
from entities.club import Club


def test_points_dashboard_with_clubs(client, monkeypatch):
    test_club = Club(name="Test Club", email="test@club.com", points=13)
    nice_club = Club(name="Nice Club", email="nice@club.com", points=8)
    club_repository = InMemoryClubRepository([test_club, nice_club])
    monkeypatch.setattr("server.club_repository", club_repository)

    response = client.get("/points-dashboard")
    assert response.status_code == 200
    assert b"Points Dashboard" in response.data
    assert b"Test Club" in response.data
    assert b"13" in response.data
    assert b"Nice Club" in response.data
    assert b"8" in response.data


def test_points_dashboard_without_clubs(client, monkeypatch):
    club_repository = InMemoryClubRepository([])
    monkeypatch.setattr("server.club_repository", club_repository)

    response = client.get("/points-dashboard")
    assert response.status_code == 200
    assert b"Points Dashboard" in response.data
    assert b"No clubs registered." in response.data
