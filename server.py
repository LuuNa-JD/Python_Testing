import json
from flask import Flask, render_template, request, redirect, flash, url_for

from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
reservations = {club['name']: {} for club in clubs}


@app.route('/')
def index(): return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [
            club for club in clubs
            if club['email'] == request.form['email']
        ][0]
        return render_template(
            'welcome.html', club=club, competitions=competitions, clubs=clubs
        )

    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    competition = next(
        (c for c in competitions if c['name'] == competition), None
    )
    club = next((c for c in clubs if c['name'] == club), None)

    competition_date = datetime.strptime(
        competition['date'], "%Y-%m-%d %H:%M:%S"
    )
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )

    return render_template('booking.html', club=club, competition=competition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [
        c for c in competitions
        if c['name'] == request.form['competition']
    ][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    competition_date = datetime.strptime(
        competition['date'], "%Y-%m-%d %H:%M:%S"
    )
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )

    elif int(competition['numberOfPlaces']) < placesRequired:
        flash("Not enough places available in the competition.")
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )

    elif int(club['points']) < placesRequired:
        flash("You do not have enough points to book that many places.")
        return redirect(
            url_for('book', competition=competition['name'], club=club['name'])
        )

    reserved_places = reservations[club['name']].get(competition['name'], 0)
    if reserved_places + placesRequired > 12:
        flash("You cannot book more than 12 places in a single competition.")
        return redirect(
            url_for('book', competition=competition['name'], club=club['name'])
        )

    club['points'] = str(int(club['points']) - placesRequired)
    competition['numberOfPlaces'] = str(
        int(competition['numberOfPlaces']) - placesRequired
    )
    reservations[club['name']][competition['name']] = (
        reserved_places + placesRequired
    )
    flash('Great - booking complete !')
    return render_template(
        'welcome.html', club=club, competitions=competitions, clubs=clubs
    )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
