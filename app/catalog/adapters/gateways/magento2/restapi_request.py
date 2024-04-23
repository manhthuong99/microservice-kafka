import os
import aiohttp


class RestApiRequest:
    def __init__(self, config=None):
        self.base_url = os.getenv('M2_BASE_URL')
        self.bearer_token = os.getenv('M2_BEARER_TOKEN')
        self.store = config.store if config else "default"
        self.version = os.getenv('M2_API_VERSION')

    def set_bearer_token(self, bearer_token):
        self.bearer_token = bearer_token

    async def do_request(self, endpoint, body=None, method="POST", is_async=True):
        if body is None:
            body = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }

        url = f"{self.base_url}/rest/{self.version}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=body) as response:
                if response.status == 200:
                    return {
                        "success": True,
                        "data": await response.json()
                    }
                else:
                    return {
                        "success": False,
                        "data": await response.text()
                    }
