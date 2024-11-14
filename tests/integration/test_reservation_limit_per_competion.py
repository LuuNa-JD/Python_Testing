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


def test_reservation_limit_per_competition(client):
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 13
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"You cannot book more than 12 places in a single competition." \
           in response.data
