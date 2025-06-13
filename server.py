import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from repositories.club_json_repository import ClubJsonRepository
from repositories.competition_json_repository import CompetitionJsonRepository
from repositories.reservation_json_repository import ReservationJsonRepository

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    email = request.form["email"]
    if email == "":
        flash("Please enter an email", "error")
        return render_template("index.html")

    try:
        clubs = ClubJsonRepository("clubs.json")
        competitions = CompetitionJsonRepository("competitions.json")
        club = clubs.find_by_email(email)
    except FileNotFoundError as ex:
        print(ex)
        flash("Error loading data. Please contact support.", "error")
        return render_template("index.html")
    except IndexError:
        flash("Email not found", "error")
        return render_template("index.html")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    clubs = ClubJsonRepository("clubs.json")
    competitions = CompetitionJsonRepository("competitions.json")

    found_club = clubs.find_by_name(club)
    found_competition = competitions.find_by_name(competition)

    if found_club and found_competition:
        return render_template("booking.html", club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    reservations = ReservationJsonRepository("reservations.json")
    clubs = ClubJsonRepository("clubs.json")
    competitions = CompetitionJsonRepository("competitions.json")

    club = clubs.find_by_name(request.form["club"])
    competition = competitions.find_by_name(request.form["competition"])
    places_required = int(request.form["places"])

    if not club.has_enough_points(places_required):
        flash("Not enough points", "error")
        return render_template("booking.html", club=club, competition=competition)

    if not competition.is_within_reservation_limit(places_required):
        flash(f"Maximum booking limit is {competition.max_places_per_reservation} places", "error")
        return render_template("booking.html", club=club, competition=competition)

    if not competition.can_reserve(places_required):
        flash("Not enough available places", "error")
        return render_template("booking.html", club=club, competition=competition)

    new_reservation = club.reserve(competition, places_required, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    reservations.add(new_reservation)
    reservations.save()
    clubs.save()
    competitions.save()

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
