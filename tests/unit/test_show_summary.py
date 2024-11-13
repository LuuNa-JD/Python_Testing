import sys
import os
import pytest
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


def test_show_summary_email_not_found(client):
    response = client.post(
        '/showSummary',
        data={'email': 'unknown@example.com'},
        follow_redirects=False
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any(
            "Sorry, that email wasn't found." in message
            for message in flashed_messages
        )
