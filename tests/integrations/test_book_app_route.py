from datetime import datetime

from entities.club import Club
from entities.competition import Competition
from tests.in_memory_repositories.in_memory_club_repository import InMemoryClubRepository
from tests.in_memory_repositories.in_memory_competition_repository import InMemoryCompetitionRepository


def test_book_with_valid_club_and_competition(client, monkeypatch):
    club = Club(name="Test Club", email="test@club.com", points=15)
    competition = Competition(name="Compétition", date=datetime(2025, 10, 1, 10, 0, 0), available_places=10)
    club_repository = InMemoryClubRepository([club])
    competition_repository = InMemoryCompetitionRepository([competition])

    monkeypatch.setattr("server.club_repository", club_repository)
    monkeypatch.setattr("server.competition_repository", competition_repository)

    with client.session_transaction() as session:
        session["club_name"] = club.name

    response = client.get(f"/book/{competition.name}/{club.name}")
    assert response.status_code == 200
    assert b"Book" in response.data and b"How many places" in response.data


def test_book_with_invalid_club(client, monkeypatch):
    competition = Competition(name="Compétition", date=datetime(2025, 10, 1, 10, 0, 0), available_places=10)
    club_repository = InMemoryClubRepository([])
    competition_repository = InMemoryCompetitionRepository([competition])

    monkeypatch.setattr("server.club_repository", club_repository)
    monkeypatch.setattr("server.competition_repository", competition_repository)

    response = client.get(f"/book/{competition.name}/unknown_club", follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data
