def test_login_with_non_existing_email(client):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 200
    assert b"Please enter an email" in response.data
