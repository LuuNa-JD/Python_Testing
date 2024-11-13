import sys
import os
import pytest
import json
sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)
from server import app, clubs, competitions # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_data():
    competitions[:] = json.load(open("competitions.json"))["competitions"]
    clubs[:] = json.load(open("clubs.json"))["clubs"]


def test_full_reservation_process(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b"Spring Festival" in response.data

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 5
    })
    assert response.status_code == 200
    assert b"Great - booking complete !" in response.data

    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    initial_points = int(club['points']) + 5
    assert int(club['points']) == initial_points - 5
