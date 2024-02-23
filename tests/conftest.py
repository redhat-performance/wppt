import pytest

from wppt.app import app as flask_app


@pytest.fixture(scope="module")
def test_client():
    """
    | Creates a test client for the app.
    """
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client