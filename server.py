import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from repositories.club_json_repository import ClubJsonRepository
from repositories.competition_json_repository import CompetitionJsonRepository
from repositories.reservation_json_repository import ReservationJsonRepository
from usecases.reservation_place import ReservePlaceUseCase

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

reservations = ReservationJsonRepository("reservations.json")
clubs = ClubJsonRepository("clubs.json")
competitions = CompetitionJsonRepository("competitions.json")

reserve_place_use_case = ReservePlaceUseCase(
    club_repository=clubs, competition_repository=competitions, reservation_repository=reservations
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["GET", "POST"])
def show_summary():
    clubs.reload()
    competitions.reload()
    date_now = datetime.now()

    if request.method == "POST":
        email = request.form["email"]
        if email == "":
            flash("Please enter an email", "error")
            return render_template("index.html")

        club = clubs.find_by_email(email)
        if not club:
            flash("Email not found", "error")
            return render_template("index.html")

        session["club_name"] = club.name

        return render_template("welcome.html", club=club, competitions=competitions.all(), date_now=date_now)

    if request.method == "GET":
        club_name = session.get("club_name")
        if not club_name:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for("index"))

        club = clubs.find_by_name(club_name)
        if not club:
            flash("club not found.", "error")
            return redirect(url_for("index"))
        return render_template("welcome.html", club=club, competitions=competitions.all(), date_now=date_now)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    clubs.reload()
    competitions.reload()
    found_club = clubs.find_by_name(club)
    found_competition = competitions.find_by_name(competition)

    if found_club and found_competition:
        return render_template("booking.html", club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions.all())


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    clubs.reload()
    competitions.reload()
    reservations.reload()

    club_name = request.form["club"]
    competition_name = request.form["competition"]
    places = request.form["places"].strip()
    date_now = datetime.now()

    if not places.isdigit():
        flash("Please enter a valid number of places", "error")
        club = clubs.find_by_name(club_name)
        competition = competitions.find_by_name(competition_name)
        return render_template("booking.html", club=club, competition=competition)

    places_required = int(places)

    try:
        reserve_place_use_case.execute(
            club_name=club_name, competition_name=competition_name, places=places_required, date=date_now
        )
        flash(f"{places_required} place(s) successfully reserved for {competition_name}!", "success")

    except ValueError as e:
        flash(str(e), "error")
        club = clubs.find_by_name(club_name)
        competition = competitions.find_by_name(competition_name)
        return render_template("booking.html", club=club, competition=competition)

    club = clubs.find_by_name(club_name)
    return render_template("welcome.html", club=club, competitions=competitions.all(), date_now=date_now)


@app.route("/points-dashboard")
def points_dashboard():
    clubs.reload()
    return render_template("points_dashboard.html", clubs=clubs.all())


@app.route("/logout")
def logout():
    session.pop("club_name", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
