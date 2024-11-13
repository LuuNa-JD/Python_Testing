import sys
import os
import pytest
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

    assert b"Great-booking complete!" in response.data

    updated_points = initial_points - places_to_purchase
    assert int(club['points']) == updated_points

    updated_places = initial_places - places_to_purchase
    assert int(competition['numberOfPlaces']) == updated_places
