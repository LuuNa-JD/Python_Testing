import pytest
import json
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_data():
    competitions[:] = json.load(open("competitions.json"))["competitions"]
    clubs[:] = json.load(open("clubs.json"))["clubs"]


def test_booking_past_competition(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    competition['date'] = "2020-03-27 10:00:00"

    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 3
    })

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    assert club['points'] == "13"  # Les points ne doivent pas changer
    assert competition['numberOfPlaces'] == "25"
