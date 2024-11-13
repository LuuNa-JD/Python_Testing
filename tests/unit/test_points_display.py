import sys
import os
import pytest
sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)

from server import app, clubs # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_points_display_on_index(client):
    response = client.get('/')
    assert response.status_code == 200

    for club in clubs:
        assert bytes(club['name'], 'utf-8') in response.data
        assert bytes(club['points'], 'utf-8') in response.data


def test_points_display_after_login(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200

    for club in clubs:
        assert bytes(club['name'], 'utf-8') in response.data
        assert bytes(club['points'], 'utf-8') in response.data
