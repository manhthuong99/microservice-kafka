from abc import abstractmethod


class MessageInterface:

    @abstractmethod
    async def init(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def create_topics(self, topics, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def send(self, topic, data, key=None, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def subscribe(self, topic, callback, key=None, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def flush(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()
