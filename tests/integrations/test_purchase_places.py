from datetime import datetime
from typing import Tuple

import pytest

from entities.club import Club
from entities.competition import Competition
from tests.in_memory_repositories.in_memory_club_repository import InMemoryClubRepository
from tests.in_memory_repositories.in_memory_competition_repository import InMemoryCompetitionRepository
from tests.in_memory_repositories.in_memory_reservation_repository import InMemoryReservationRepository
from usecases.reservation_place import ReservePlaceUseCase


@pytest.fixture
def default_club():
    return Club(name="Test Club", email="test@club.com", points=13)


@pytest.fixture
def future_competition():
    return Competition(name="Future Competition", date=datetime(2025, 10, 1, 10, 0, 0), available_places=10)


@pytest.fixture
def past_competition():
    return Competition(name="Test Competition", date=datetime(2024, 10, 1, 10, 0, 0), available_places=15)


def setup_use_case(
    club: Club, competition: Competition, monkeypatch: pytest.MonkeyPatch
) -> Tuple[InMemoryClubRepository, InMemoryCompetitionRepository, InMemoryReservationRepository]:
    club_repository = InMemoryClubRepository([club])
    competition_repository = InMemoryCompetitionRepository([competition])
    reservation_repository = InMemoryReservationRepository()
    reservation_use_case = ReservePlaceUseCase(club_repository, competition_repository, reservation_repository)

    monkeypatch.setattr("server.club_repository", club_repository)
    monkeypatch.setattr("server.competition_repository", competition_repository)
    monkeypatch.setattr("server.reservation_repository", reservation_repository)
    monkeypatch.setattr("server.reserve_place_use_case", reservation_use_case)

    return club_repository, competition_repository, reservation_repository


def test_purchase_places_success(client, monkeypatch, default_club, future_competition):
    """Test successful reservation of places for a competition."""
    setup_use_case(default_club, future_competition, monkeypatch)
    reserved_places = "5"

    with client.session_transaction() as session:
        session["club_name"] = default_club.name

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert f"{reserved_places} place(s) successfully reserved for {future_competition.name}!" in response.data.decode()
    assert future_competition.available_places == 5
    assert default_club.points == 8


def test_purchase_places_fails_with_invalid_input(client, monkeypatch, default_club, future_competition):
    setup_use_case(default_club, future_competition, monkeypatch)
    invalid_input = "abcd"  # Non-numeric input

    with client.session_transaction() as session:
        session["club_name"] = default_club.name

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": invalid_input},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Please enter a valid number of places" in response.data


def test_purchase_places_fails_with_club_not_found(client, monkeypatch, default_club, future_competition):
    setup_use_case(default_club, future_competition, monkeypatch)

    response = client.post(
        "/purchasePlaces",
        data={"club": "unknown_club", "competition": future_competition.name, "places": "5"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Club not found." in response.data


def test_purchase_places_fails_with_competition_not_found(client, monkeypatch, default_club, future_competition):
    setup_use_case(default_club, future_competition, monkeypatch)

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": "unknown_competition", "places": "5"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Competition not found." in response.data


def test_purchase_places_fails_with_zero_places(client, monkeypatch, default_club, future_competition):
    setup_use_case(default_club, future_competition, monkeypatch)
    reserved_places = "0"

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Number of places must be greater than zero." in response.data


def test_purchase_places_fails_with_club_reserved_greater_than_available_places(
    client, monkeypatch, default_club, future_competition
):
    setup_use_case(default_club, future_competition, monkeypatch)
    reserved_places = "11"

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Not enough available places in the competition." in response.data


def test_purchase_places_fails_with_club_not_enough_points(client, monkeypatch, default_club, future_competition):
    setup_use_case(default_club, future_competition, monkeypatch)
    reserved_places = "14"

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Club does not have enough points to reserve places." in response.data


def test_purchase_places_fails_with_past_competition(client, monkeypatch, default_club, past_competition):
    setup_use_case(default_club, past_competition, monkeypatch)
    reserved_places = "5"

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": past_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Cannot reserve places for a past competition." in response.data


def test_purchase_places_fails_with_exceding_max_per_club(client, monkeypatch, default_club, future_competition):
    _, _, reservation_repository = setup_use_case(default_club, future_competition, monkeypatch)
    reserved_places = "3"

    reservation_repository.save(
        default_club.reserve(future_competition, 10, datetime.now())
    )  # Simulate existing reservation of 10 places

    total_already_reserved = reservation_repository.get_total_places_club_reservation_for_competition(
        default_club.id, future_competition.id
    )

    remaining_quota = future_competition.max_places_per_reservation - total_already_reserved

    response = client.post(
        "/purchasePlaces",
        data={"club": default_club.name, "competition": future_competition.name, "places": reserved_places},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        f"You have already reserved {total_already_reserved} place(s). You can only reserve {remaining_quota} more."
    ) in response.data.decode()
