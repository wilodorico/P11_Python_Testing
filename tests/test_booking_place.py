from globals import LIMITED_BOOKING_PLACE


def get_mock_clubs(points: str):
    return {"clubs": [{"email": "clubtest@test.com", "name": "Club Test", "points": points}]}


def get_mock_competitions(places: str):
    return {"competitions": [{"name": "Competition Test", "date": "2020-03-27 10:00:00", "numberOfPlaces": places}]}


def test_club_cannot_book_more_than_points(client, mocker):
    mock_clubs = get_mock_clubs("5")
    mock_competitions = get_mock_competitions("10")

    mocker.patch("server.JSONServices.load", side_effect=[mock_clubs, mock_competitions])

    response = client.post(
        "/purchasePlaces", data={"competition": "Competition Test", "club": "Club Test", "places": "6"}
    )

    assert response.status_code == 200
    assert b"Not enough points" in response.data


def test_club_cannot_book_more_than_limit(client, mocker):
    places_requested = str(LIMITED_BOOKING_PLACE + 1)
    club_points = str(LIMITED_BOOKING_PLACE + 5)
    number_of_competition_places = str(LIMITED_BOOKING_PLACE + 5)
    mock_clubs = get_mock_clubs(club_points)
    mock_competitions = get_mock_competitions(number_of_competition_places)

    mocker.patch("server.JSONServices.load", side_effect=[mock_clubs, mock_competitions])

    response = client.post(
        "/purchasePlaces", data={"competition": "Competition Test", "club": "Club Test", "places": places_requested}
    )

    assert response.status_code == 200
    assert f"Maximum booking limit is {LIMITED_BOOKING_PLACE} places".encode() in response.data


def test_competition_places_are_deducted_when_club_books(client, mocker):
    mock_clubs = get_mock_clubs(points="15")
    mock_competitions = get_mock_competitions(places="20")
    places_requested = "5"

    mocker.patch("server.JSONServices.load", side_effect=[mock_clubs, mock_competitions])
    mocker.patch("json_services.open", mocker.mock_open())

    mock_json_dump = mocker.patch("json.dump")

    response = client.post(
        "/purchasePlaces", data={"competition": "Competition Test", "club": "Club Test", "places": places_requested}
    )

    assert response.status_code == 200

    called_data = mock_json_dump.call_args[0][0]
    competitions = called_data["competitions"]

    updated = next(c for c in competitions if c["name"] == "Competition Test")
    assert updated["numberOfPlaces"] == "15"
