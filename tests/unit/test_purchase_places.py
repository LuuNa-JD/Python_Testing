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
    # Recharge les données initiales pour chaque test
    competitions[:] = json.load(open("competitions.json"))["competitions"]
    clubs[:] = json.load(open("clubs.json"))["clubs"]


def test_purchase_places_not_enough_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': 5
    })
    assert b"You do not have enough points to book that many places." \
           in response.data
    club = next(c for c in clubs if c['name'] == 'Iron Temple')
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    assert str(club['points']) == "4"
    assert str(competition['numberOfPlaces']) == "25"


def test_purchase_places_successful(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': 2
    })

    assert b"Great - booking complete !" in response.data

    club = next(c for c in clubs if c['name'] == 'Iron Temple')
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    assert str(club['points']) == "2"
    assert str(competition['numberOfPlaces']) == "23"


def test_purchase_places_exceeds_max_limit(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 13
    })
    assert b"You cannot book more than 12 places in a single competition." \
           in response.data
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    assert competition['numberOfPlaces'] == "25"


def test_purchase_places_within_max_limit(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 12
    })
    assert b"Great - booking complete !" in response.data
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    assert competition['numberOfPlaces'] == "13"


def test_purchase_places_updates_club_points(client):
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )

    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])
    places_to_purchase = 3

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': places_to_purchase
    })

    assert b"Great - booking complete !" in response.data

    updated_points = initial_points - places_to_purchase
    assert int(club['points']) == updated_points

    updated_places = initial_places - places_to_purchase
    assert int(competition['numberOfPlaces']) == updated_places


def test_purchase_places_no_places_left(client):
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    competition['numberOfPlaces'] = "0"

    client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 1
    })
    assert competition['numberOfPlaces'] == "0"
