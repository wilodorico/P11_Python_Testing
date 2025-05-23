def test_club_cannot_book_more_than_points(client, mocker):
    mock_clubs = {"clubs": [{"email": "clubtest@test.com", "name": "Club Test", "points": "5"}]}

    mock_competitions = {
        "competitions": [{"name": "Competition Test", "date": "2020-03-27 10:00:00", "numberOfPlaces": "10"}]
    }

    mocker.patch("server.JSONServices.load", side_effect=[mock_clubs, mock_competitions])

    response = client.post(
        "/purchasePlaces", data={"competition": "Competition Test", "club": "Club Test", "places": "6"}
    )

    assert response.status_code == 200
    assert b"Not enough points" in response.data
