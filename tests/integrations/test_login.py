def test_login_without_email(client):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 200
    assert b"Please enter an email" in response.data


def test_login_with_non_existent_email(client):
    response = client.post("/showSummary", data={"email": "nonexistent@test.com"})
    assert response.status_code == 200
    assert b"Email not found" in response.data
