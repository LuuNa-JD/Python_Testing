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
