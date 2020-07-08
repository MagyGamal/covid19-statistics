import os
import tempfile
import pytest
from flaskr import app


@pytest.fixture
def client():
    """A test client for the app."""
    return app.test_client()


def test_home(client):
    assert client.get("/").status_code == 200


def test_single_response(client):
    assert client.get("/?country=egypt&status=recovered&graph=Bars").status_code == 200


def test_comparison_response(client):
    assert client.get("/?country_2=egypt&country_1=algeria&status=deaths").status_code == 200


