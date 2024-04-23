from .event_base import EventBase


async def execute(data):
    event_base = EventBase()
    await event_base.make_request(endpoint="products", method="POST", params=data)
