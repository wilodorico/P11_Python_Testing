import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

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


@app.route("/showSummary", methods=["POST"])
def show_summary():
    clubs.reload()
    competitions.reload()

    email = request.form["email"]
    if email == "":
        flash("Please enter an email", "error")
        return render_template("index.html")

    club = clubs.find_by_email(email)
    if not club:
        flash("Email not found", "error")
        return render_template("index.html")

    return render_template("welcome.html", club=club, competitions=competitions)


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
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    club_name = request.form["club"]
    competition_name = request.form["competition"]
    places_required = int(request.form["places"])
    date = datetime.now()

    try:
        reserve_place_use_case.execute(
            club_name=club_name, competition_name=competition_name, places=places_required, date=date
        )
        flash(f"{places_required} place(s) successfully reserved for {competition_name}!", "success")

    except ValueError as e:
        flash(str(e), "error")
        club = clubs.find_by_name(club_name)
        competition = competitions.find_by_name(competition_name)
        return render_template("booking.html", club=club, competition=competition)

    club = clubs.find_by_name(club_name)
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
