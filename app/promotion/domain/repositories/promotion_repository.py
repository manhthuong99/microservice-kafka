from abc import abstractmethod


class PromotionRepository:

    async def init(self):
        pass

    @abstractmethod
    async def get(self, coupon):
        raise NotImplementedError()

    @abstractmethod
    async def save(self, promotion):
        raise NotImplementedError()

    @abstractmethod
    async def apply(self, coupon):
        raise NotImplementedError()
