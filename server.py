import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from globals import LIMITED_BOOKING_PLACE
from json_services import JSONServices

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
    clubs = JSONServices.load("clubs.json")["clubs"]
    competitions = JSONServices.load("competitions.json")["competitions"]
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    club_points = int(club["points"])

    if placesRequired > club_points:
        flash("Not enough points", "error")
        return render_template("booking.html", club=club, competition=competition)

    if placesRequired > LIMITED_BOOKING_PLACE:
        flash(f"Maximum booking limit is {LIMITED_BOOKING_PLACE} places", "error")
        return render_template("booking.html", club=club, competition=competition)

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
