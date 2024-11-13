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


def test_book_past_competition(client):
    competition = next(
        c for c in competitions if c['name'] == 'Spring Festival'
    )
    competition['date'] = "2020-03-27 10:00:00"

    response = client.get(
        '/book/Spring Festival/Simply Lift', follow_redirects=True
    )

    assert b"You cannot book places for a past competition." in response.data

    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    assert club['points'] == "13"
    assert competition['numberOfPlaces'] == "25"
