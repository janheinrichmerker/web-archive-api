from datetime import datetime, timezone
from re import match

from web_archive_api.memento import MementoApi


def test_google_2023_response():
    api = MementoApi("https://web.archive.org/web")
    url = "https://www.google.com/"
    timestamp = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    response = api.load_url(url, timestamp)
    assert response is not None
    assert match(
        r"https://web\.archive\.org/web/20230101000000/"
        r"https?://?www\.google\.com/",
        response.url)
    assert response.status_code == 200
    assert response.text.startswith("<!doctype html>")


def test_google_2023_warc():
    api = MementoApi("https://web.archive.org/web")
    url = "https://www.google.com/"
    timestamp = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    records = api.load_url_warc(url, timestamp)
    assert len(records) == 2
    assert records[0].rec_type == "request"
    assert records[0].content_type == "application/http"
    assert records[1].rec_type == "response"
    assert records[1].content_type == "application/http"
