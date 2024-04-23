import aiohttp

from loguru import logger


class RestApi:

    async def do_request(self, url, method="GET", params=None, header=None, *args, **kwargs):
        headers = {"Content-Type": "application/json"}

        if header is not None:
            headers.update(header)

        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url=url, headers=headers, params=params) as response:
                    result = await self.handle_response(response)
            elif method == "POST":
                async with session.post(url=url, headers=headers, data=params) as response:
                    result = await self.handle_response(response)
            elif method == "PUT":
                async with session.put(url=url, headers=headers, data=params) as response:
                    result = await self.handle_response(response)
            elif method == "DELETE":
                async with session.delete(url=url, headers=headers, params=params) as response:
                    result = await self.handle_response(response)
            else:
                raise f"Method {method} not allow"

            return result

    async def handle_response(self, response):
        if response.status == 200:
            return await response.json()
        else:
            logger.info(f"Request failed. Code: {response.status} Message: {await response.text()}")
            return False
