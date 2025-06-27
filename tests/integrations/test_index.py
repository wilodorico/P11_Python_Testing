def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Login" in response.data or b"Points Dashboard" in response.data
