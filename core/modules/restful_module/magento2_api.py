import aiohttp
from loguru import logger
from .rest_base import RestBase


class Magento2Api(RestBase):

    async def init(self, base_url, bearer_token, api_version, store=None):
        self.api_base_url = base_url
        self.api_authentication_key = bearer_token
        self.api_version = api_version
        self.store = store if store is not None else "default"

    async def do_request(self, endpoint, params=None, method="GET"):
        params = params if params is not None else {}
        url = f"{self.api_base_url}/rest/{self.api_version}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_authentication_key}"
        }
        return await self.execute_request(url=url, headers=headers, params=params, method=method)
