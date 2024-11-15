import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_logout(client):
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
