import pytest
import time
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_competitions_load_time(client):
    start_time = time.time()
    response = client.get('/')
    assert response.status_code == 200
    load_time = time.time() - start_time
    assert load_time < 5, (
        (
            f"Competitions loaded in {load_time:.2f} seconds, "
            "should be < 5 seconds"
        )
    )
