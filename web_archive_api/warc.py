from io import BytesIO
from typing import Iterator, Sequence, Mapping, IO
from urllib.parse import urlsplit, SplitResult

from requests import Response, PreparedRequest
from warcio.recordbuilder import RecordBuilder
from warcio.recordloader import ArcWarcRecord, StatusAndHeaders


def _get_proxy_information(response: Response) -> Mapping[str, str]:
    connection = getattr(response, "connection", None)
    if connection is None:
        return {}

    proxy_manager = getattr(connection, "proxy_manager", None)
    if proxy_manager is None:
        return {}

    request_url = response.request.url
    if request_url is None:
        return {}

    proxy_info = {
        "request_path": request_url,
    }
    if request_url.startswith("https://"):
        proxy_info["method"] = "CONNECT"
    return proxy_info


def _build_request_path(
        parsed_url: SplitResult,
        proxy_info: Mapping[str, str],
) -> str:
    proxy_url = proxy_info.get("request_path")
    if proxy_url is not None:
        request_path = proxy_url
        return request_path

    request_path = parsed_url.path
    if parsed_url.query:
        request_path += f"?{parsed_url.query}"

    return request_path


def _request_record(
        request: PreparedRequest,
        proxy_info: Mapping[str, str],
        record_builder: RecordBuilder
) -> ArcWarcRecord:
    if request.url is None:
        raise ValueError("Request URL not given.")

    parsed_url: SplitResult = urlsplit(request.url)
    method: str
    if "method" in proxy_info:
        method = proxy_info["method"]
    elif request.method is not None:
        method = request.method
    else:
        raise ValueError("Request method not given.")

    request_path: str = _build_request_path(parsed_url, proxy_info)
    protocol = "HTTP/1.1"
    status_line = f"{method} {request_path} {protocol}"

    # <prefix>Host: <request-host> OR host header specified by user
    headers = request.headers.copy()
    if "Host" not in headers:
        headers["Host"] = parsed_url.netloc

    payload: IO[bytes]
    if request.body is None:
        payload = BytesIO()
    elif isinstance(request.body, bytes):
        payload = BytesIO(request.body)
    elif isinstance(request.body, str):
        payload = BytesIO(request.body.encode("utf-8"))
    else:
        raise ValueError(f"Unexpected request body type: {type(request.body)}")

    return record_builder.create_warc_record(
        record_type="request",
        warc_content_type="application/http",
        uri=request.url,
        payload=payload,
        length=None,  # Let warcio recompute the content length and digest.
        http_headers=StatusAndHeaders(
            statusline=status_line,
            headers=headers,
            protocol=protocol,
        ),
    )


_HTTP_VERSIONS = {
    9: "0.9",
    10: "1.0",
    11: "1.1",
}


def _response_record(
        response: Response,
        record_builder: RecordBuilder,
) -> ArcWarcRecord:
    version = _HTTP_VERSIONS.get(response.raw.version, "?")
    protocol = f"HTTP/{version}"
    status_line = f"{protocol} {response.status_code} {response.reason}"

    return record_builder.create_warc_record(
        record_type="response",
        warc_content_type="application/http",
        uri=response.url,
        payload=BytesIO(response.content),
        length=None,  # Let warcio recompute the content length and digest.
        http_headers=StatusAndHeaders(
            statusline=status_line,
            headers=response.headers,
            protocol=protocol,
        ),
    )


def iter_warc_records(
        response: Response,
        record_builder: RecordBuilder = RecordBuilder(),
) -> Iterator[ArcWarcRecord]:
    """
    For an HTTP response, yield WARC records describing all intermediate
    HTTP requests and HTTP responses.
    :param response: HTTP response.
    :param record_builder: Optional WARC record builder.
    :return: Iterator of WARC records.
    """
    history = [*response.history, response]
    for intermediate_response in history:
        proxy_information = _get_proxy_information(intermediate_response)
        yield _request_record(
            intermediate_response.request,
            proxy_information,
            record_builder,
        )
        yield _response_record(
            intermediate_response,
            record_builder,
        )


def get_warc_records(
        response: Response,
        record_builder: RecordBuilder = RecordBuilder(),
) -> Sequence[ArcWarcRecord]:
    """
    For an HTTP response, get a sequence of WARC records describing all
    intermediate HTTP requests and HTTP responses.
    :param response: HTTP response.
    :param record_builder: Optional WARC record builder.
    :return: Sequence of WARC records.
    """
    return tuple(iter_warc_records(
        response=response,
        record_builder=record_builder,
    ))
