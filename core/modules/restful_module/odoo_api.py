from .rest_base import RestBase


class OdooApi(RestBase):


    async def init(self, base_url, access_token):
        self.api_base_url = base_url
        self.access_token = access_token

    async def do_request(self, endpoint, params=None, method="GET"):
        url = f"{self.api_base_url}/api/{endpoint}"
        headers = {
            "Authorization": f"{self.access_token}"
        }
        return await self.execute_request(url=url, headers=headers, params=params, method=method)
