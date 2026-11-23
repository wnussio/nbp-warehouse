import pytest

from datetime import date

import requests

from nbp_warehouse.nbp_client import fetch_tables


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []          # zapamiętuje, z czym ją wołano

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response

@pytest.fixture
def payload():
    return [{"table": "A", "effectiveDate": "2024-01-02", "rates": []}]

def test_returns_url_and_data(payload):
    session = FakeSession(FakeResponse(200, payload))

    url, data = fetch_tables(session, date(2024, 1, 2), date(2024, 1, 5))

    assert data == payload
    assert url == 'https://api.nbp.pl/api/exchangerates/tables/A/2024-01-02/2024-01-05/'

def test_404_means_no_data():
    session = FakeSession(FakeResponse(404))

    url, data = fetch_tables(session, date(2024, 1, 6), date(2024, 1, 7))

    assert data == []

def test_server_error_raises():
    session = FakeSession(FakeResponse(500))

    with pytest.raises(requests.HTTPError):
        fetch_tables(session, date(2024, 1, 2), date(2024, 1, 5))

def test_sends_timeout():
    session = FakeSession(FakeResponse(200, []))

    fetch_tables(session, date(2024, 1, 2), date(2024, 1, 5))

    url, kwargs = session.calls[0]
    assert kwargs['timeout'] == 10

