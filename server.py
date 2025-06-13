import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from json_services import JSONServices
from models.club import Club
from models.competition import Competition
from repositories.reservation_json_repository import ReservationJsonRepository

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"]
    if email == "":
        flash("Please enter an email", "error")
        return render_template("index.html")

    try:
        clubs = JSONServices.load("clubs.json")["clubs"]
        competitions = JSONServices.load("competitions.json")["competitions"]
        club = [club for club in clubs if club["email"] == email][0]
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
    clubs = JSONServices.load("clubs.json")["clubs"]
    competitions = JSONServices.load("competitions.json")["competitions"]
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    clubs_data = JSONServices.load("clubs.json")["clubs"]
    competitions_data = JSONServices.load("competitions.json")["competitions"]

    clubs = [Club.deserialize(c) for c in clubs_data]
    competitions = [Competition.deserialize(c) for c in competitions_data]

    reservations = ReservationJsonRepository("reservations.json")

    club = next((c for c in clubs if c.name == request.form["club"]), None)
    competition = next((c for c in competitions if c.name == request.form["competition"]), None)
    placesRequired = int(request.form["places"])

    if not club.has_enough_points(placesRequired):
        flash("Not enough points", "error")
        return render_template("booking.html", club=club, competition=competition)

    if not competition.is_within_reservation_limit(placesRequired):
        flash(f"Maximum booking limit is {competition.max_places_per_reservation} places", "error")
        return render_template("booking.html", club=club, competition=competition)

    if not competition.can_reserve(placesRequired):
        flash("Not enough available places", "error")
        return render_template("booking.html", club=club, competition=competition)

    new_reservation = club.reserve(competition, placesRequired, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    reservations.add(new_reservation)
    reservations.save()

    clubs = [c.serialize() for c in clubs]
    competitions = [c.serialize() for c in competitions]

    JSONServices.save("clubs.json", {"clubs": clubs})
    JSONServices.save("competitions.json", {"competitions": competitions})

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
