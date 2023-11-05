from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterator, NamedTuple, Optional, Union
from urllib.parse import urljoin

from requests import Session, Response
from warcio.archiveiterator import ArchiveIterator
from warcio.capture_http import capture_http
from warcio.recordloader import ArcWarcRecord

from web_archive_api.cdx import CdxCapture


class _TimestampUrl(NamedTuple):
    url: str
    timestamp: Optional[datetime]


@dataclass(frozen=True)
class MementoApi:
    """
    Client to download captured documents from a web archive's Memento API.
    """
    api_url: str
    """
    URL of the Memento API endpoint (e.g. https://web.archive.org/web/).
    """
    session: Session = Session()
    """
    HTTP session to use for requests.
    (Useful for setting headers, proxies, rate limits, etc.)
    """
    quiet: bool = False
    """
    Suppress all output and progress bars.
    """

    def _load(
            self,
            url_or_cdx_capture: Union[_TimestampUrl, CdxCapture],
            raw: bool,
    ) -> Response:
        if isinstance(url_or_cdx_capture, _TimestampUrl):
            url = url_or_cdx_capture.url
            timestamp = url_or_cdx_capture.timestamp
        elif isinstance(url_or_cdx_capture, CdxCapture):
            url = url_or_cdx_capture.url
            timestamp = url_or_cdx_capture.timestamp
        else:
            raise ValueError(
                f"Illegal argument type: {type(url_or_cdx_capture)}")
        if timestamp is None:
            memento_timestamp = "*"
        else:
            memento_timestamp = (
                timestamp.astimezone(timezone.utc).strftime("%Y%m%d%H%M%S"))
        memento_raw_suffix = "id_" if raw else ""
        memento_path = f"{memento_timestamp}{memento_raw_suffix}/{url}"
        memento_raw_url = urljoin(self.api_url, memento_path)
        response = self.session.get(memento_raw_url)
        response.raise_for_status()
        return response

    def load_url(
            self,
            url: str,
            timestamp: Optional[datetime] = None,
            raw: bool = False,
    ) -> Response:
        """
        Load a captured document from the Memento API.
        :param url: The original URL of the document.
        :param timestamp: Timestamp of the capture.
        :param raw: Whether to return the raw archived contents or
          the rewritten (e.g., links mapped to archived versions) contents.
        :return: HTTP response.
        """
        return self._load(_TimestampUrl(url, timestamp), raw)

    def load_capture(
            self,
            capture: CdxCapture,
            raw: bool = False,
    ) -> Response:
        """
        Load a captured document from the Memento API.
        :param capture: The CDX record describing the capture.
        :param raw: Whether to return the raw archived contents or
          the rewritten (e.g., links mapped to archived versions) contents.
        :return: HTTP response.
        """
        return self._load(capture, raw)

    def _load_warc(
            self,
            url_or_cdx_capture: Union[_TimestampUrl, CdxCapture],
            raw: bool,
    ) -> Iterator[ArcWarcRecord]:
        with capture_http() as writer:
            self._load(url_or_cdx_capture, raw)
            yield from ArchiveIterator(writer.get_stream())

    def load_url_warc(
            self,
            url: str,
            timestamp: Optional[datetime] = None,
            raw: bool = False,
    ) -> Iterator[ArcWarcRecord]:
        """
        Load a captured document from the Memento API and
        capture the HTTP request and response as WARC records.
        :param url: The original URL of the document.
        :param timestamp: Timestamp of the capture.
        :param raw: Whether to return the raw archived contents or
          the rewritten (e.g., links mapped to archived versions) contents.
        :return: Iterator over request and response WARC records.
        """
        return self._load_warc(_TimestampUrl(url, timestamp), raw)

    def load_capture_warc(
            self,
            capture: CdxCapture,
            raw: bool = False,
    ) -> Iterator[ArcWarcRecord]:
        """
        Load a captured document from the Memento API and
        capture the HTTP request and response as WARC records.
        :param capture: The CDX record describing the capture.
        :param raw: Whether to return the raw archived contents or
          the rewritten (e.g., links mapped to archived versions) contents.
        :return: Iterator over request and response WARC records.
        """
        return self._load_warc(capture, raw)
