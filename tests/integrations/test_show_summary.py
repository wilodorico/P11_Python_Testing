import datetime

from adapters.in_memory_club_repository import InMemoryClubRepository
from adapters.in_memory_competition_repository import InMemoryCompetitionRepository
from entities.club import Club
from entities.competition import Competition


def test_login_without_email(client):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 200
    assert b"Please enter an email" in response.data


def test_login_with_non_existent_email(client):
    response = client.post("/showSummary", data={"email": "nonexistent@test.com"})
    assert response.status_code == 200
    assert b"Email not found" in response.data


def test_login_with_valid_email(client, monkeypatch):
    club = Club(name="Test Club", email="test@club.com", points=15)
    club_repository = InMemoryClubRepository([club])
    monkeypatch.setattr("server.club_repository", club_repository)

    response = client.post("/showSummary", data={"email": club.email})
    assert response.status_code == 200
    assert b"test@club.com" in response.data


def test_show_summary_get_without_login(client):
    response = client.get("/showSummary")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_show_summary_get_with_login(client, monkeypatch):
    club = Club(name="Test Club", email="test@club.com", points=15)
    competition = Competition(name="Compétition", date=datetime.datetime(2025, 10, 1, 10, 0, 0), available_places=10)
    club_repository = InMemoryClubRepository([club])
    competition_repository = InMemoryCompetitionRepository([competition])

    monkeypatch.setattr("server.club_repository", club_repository)
    monkeypatch.setattr("server.competition_repository", competition_repository)

    with client.session_transaction() as session:
        session["club_name"] = club.name

    response = client.get("/showSummary")
    assert response.status_code == 200
    assert b"test@club.com" in response.data


def test_show_summary_get_with_unknown_club(client, monkeypatch):
    club_repository = InMemoryClubRepository([])
    monkeypatch.setattr("server.club_repository", club_repository)

    with client.session_transaction() as session:
        session["club_name"] = "Unknown Club"

    response = client.get("/showSummary", follow_redirects=True)
    assert response.status_code == 200
    assert b"club not found" in response.data
