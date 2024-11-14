import sys
import os
import pytest
sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)
from server import app, clubs, competitions  # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_large_user_flow(client):
    response = client.post(
        '/showSummary', data={'email': 'kate@shelifts.co.uk'}
    )
    assert response.status_code == 200
    assert b"Welcome, kate@shelifts.co.uk" in response.data

    response = client.get('/book/Spring Festival/She Lifts')
    assert response.status_code == 200
    assert b"Spring Festival" in response.data

    club = next(c for c in clubs if c['name'] == 'She Lifts')
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'She Lifts',
        'places': 15
    }, follow_redirects=True)
    assert b"You do not have enough points to book that many places." \
           in response.data

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'She Lifts',
        'places': 3
    })
    assert b"Great - booking complete !" in response.data

    assert int(club['points']) == initial_points - 3
    assert int(competition['numberOfPlaces']) == initial_places - 3
