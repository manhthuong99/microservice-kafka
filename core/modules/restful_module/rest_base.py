import aiohttp
from loguru import logger
from urllib.parse import urlencode
from typing import Optional, Dict, Any


class RestBase:

    async def execute_request(self, url: str, headers: Optional[Dict[str, str]] = None,
                              params: Optional[Dict[str, Any]] = None, method: str = "GET"):
        # Set default headers
        headers = headers or {}
        logger.info(f"Execute API: {url}")
        logger.info(f"Params: {params}")
        async with aiohttp.ClientSession() as session:
            if method in {"GET", "DELETE"}:
                url = self._build_get_url(url, params)
                response = await session.get(url=url, headers=headers)
            elif method in {"POST", "PUT", "PATCH"}:
                response = await session.request(method=method, url=url, headers=headers, json=params)
            else:
                raise ValueError(f"Method {method} not allowed")

            return await self._handle_response(response)

    def _build_get_url(self, url: str, params: Dict[str, Any]) -> str:
        # Convert the params dictionary to a URL-encoded query string
        if params:
            query_string = urlencode(params)
            return f"{url}?{query_string}"
        return url

    async def _handle_response(self, response):
        response_json = {
            "status": False
        }
        try:
            if response.status == 200:
                response_json = {
                    "status": True,
                    "data": await response.json()
                }
            else:
                logger.info(f"Request failed. Code: {response.status} Message: {await response.text()}")
        except aiohttp.ContentTypeError:
            logger.error("Failed to parse JSON data in the response.")
        logger.info(f"Response: {response_json}")
        return response_json
