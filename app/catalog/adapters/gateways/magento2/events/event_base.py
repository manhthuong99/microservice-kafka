import os
from loguru import logger
from core.data.rest_api import RestApi


class EventBase(RestApi):

    def __init__(self, store=None):
        self.api_base_url = os.getenv('M2_BASE_URL')
        self.api_authentication_key = os.getenv('M2_BEARER_TOKEN')
        self.api_version = os.getenv('M2_API_VERSION')
        self.store = store if store is not None else "default"

    async def make_request(self, endpoint, params=None, method="GET", ):
        data = params if params is not None else {}
        url = f"{self.api_base_url}/rest/{self.api_version}/{endpoint}"
        header = {
            "Authorization": f"Bearer {self.api_authentication_key}"
        }
        result = await self.do_request(url=url, method=method, header=header, params=data)
        logger.info(f"Result: {result}")
