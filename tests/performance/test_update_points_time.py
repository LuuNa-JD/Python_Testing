import sys
import os
import pytest
import time
sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)
from server import app # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_update_points_time(client):
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    start_time = time.time()
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 2
    })
    assert response.status_code == 200
    update_time = time.time() - start_time
    assert update_time < 2, (
        f"Points update took {update_time:.2f} seconds, "
        "should be < 2 seconds"
    )
