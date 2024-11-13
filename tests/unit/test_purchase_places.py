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

    assert b"Great - booking complete!" in response.data

    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    assert competition['numberOfPlaces'] == "13"
