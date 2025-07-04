import random

from locust import HttpUser, between, task


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Initialize the test session with a login."""
        self.email = "john@simplylift.co"
        self.club = "Simply Lift"
        self.competition = "Summer Challenge"
        self.date_now = "2025-07-01"

        # index page
        self.client.get("/")

        # Login via POST (as in your login form)
        response = self.client.post("/showSummary", data={"email": self.email})
        if "Email not found" in response.text:
            print("Email non reconnu !")

    @task
    def reserve_places(self):
        """Simulates booking between 1 and 3 places."""
        places = str(random.randint(1, 3))
        self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club,
                "competition": self.competition,
                "places": places,
            },
        )

    @task
    def view_dashboard(self):
        self.client.get("/points-dashboard")
