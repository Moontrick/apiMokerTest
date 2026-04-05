from typing import Optional, Dict, Any, Union
import requests
from requests import Response
from .utils.logger import get_logger
from .utils.decorators import log_request, retry

logger = get_logger(__name__)


class APIClient:

    def __init__(
        self,
        base_url: str = "https://apimocker.com",
        timeout: int = 10,
        max_retries: int = 3,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        logger.info(f"APIClient initialized with base_url: {self.base_url}")

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    @retry(max_attempts=3, delay=1, backoff=1.5)
    @log_request
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        url = self._build_url(endpoint)
        logger.debug(f"GET request to {url} with params={params}")
        
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        
        self._log_response(response)
        return response

    @retry(max_attempts=3, delay=1, backoff=1.5)
    @log_request
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict, list]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        url = self._build_url(endpoint)
        logger.debug(f"POST request to {url} with data={data}, json={json}")
        
        response = self.session.post(
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )
        
        self._log_response(response)
        return response

    @retry(max_attempts=3, delay=1, backoff=1.5)
    @log_request
    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        url = self._build_url(endpoint)
        logger.debug(f"PUT request to {url} with json={json}")
        
        response = self.session.put(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )
        
        self._log_response(response)
        return response

    @retry(max_attempts=3, delay=1, backoff=1.5)
    @log_request
    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        url = self._build_url(endpoint)
        logger.debug(f"PATCH request to {url} with json={json}")
        
        response = self.session.patch(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )
        
        self._log_response(response)
        return response

    @retry(max_attempts=3, delay=1, backoff=1.5)
    @log_request
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        url = self._build_url(endpoint)
        logger.debug(f"DELETE request to {url}")
        
        response = self.session.delete(
            url,
            headers=headers,
            timeout=self.timeout,
        )
        
        self._log_response(response)
        return response

    def _log_response(self, response: Response) -> None:
        logger.info(
            f"Response: status_code={response.status_code}, "
            f"headers={dict(response.headers)}"
        )
        if response.status_code >= 400:
            logger.warning(f"Error response: {response.text}")

    def close(self) -> None:
        self.session.close()
        logger.info("APIClient session closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
