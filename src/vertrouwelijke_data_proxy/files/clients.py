import logging
from urllib.parse import urlparse

import requests
from more_ds.network import URL
from rest_framework.request import Request

logger = logging.getLogger(__name__)

USER_AGENT = "Amsterdam-Vertrouwelijke-Data-Proxy/1.0"


class ConfidentialDataClient:
    def __init__(self, base_url: URL) -> None:
        """Initialize the client configuration.

        :param base_url: Base URL of the Search Backend
        """
        if not base_url:
            raise ValueError(f"Missing {self.__class__.__name__} Base URL")
        self.base_url = base_url
        self._host = urlparse(base_url).netloc
        self._session = requests.Session()

    def call(self, request: Request) -> requests.Response:
        response = self._call(request.path)

        self._remove_hop_by_hop_headers(response)
        return response

    def _remove_hop_by_hop_headers(self, response: requests.Response) -> requests.Response:
        """
        Remove headers which should not be tunneled through:
        https: // datatracker.ietf.org / doc / html / rfc2616  # section-13.5.1
        """
        excluded_headers = {
            "connection",
            "keep-alive",
            "proxy-authenticate",
            "proxy-authorization",
            "te",
            "trailers",
            "transfer-encoding",
            "upgrade",
            "content-encoding",
            "content-length",
        }

        for header in excluded_headers:
            response.headers.pop(header, None)

        return response

    def _call(self, path) -> requests.Response:
        return self._session.request(
            "GET",
            f"{self.base_url}{path}",
        )
