def test_logout_clears_session_and_redirect(client):
    with client.session_transaction() as session:
        session["club_name"] = "Test Club"

    response = client.get("/logout", follow_redirects=True)

    with client.session_transaction() as session:
        assert "club_name" not in session

    assert response.status_code == 200
    assert b"You have been logged out." in response.data
