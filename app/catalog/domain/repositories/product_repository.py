from abc import abstractmethod
from ..entities.product import Product


class ProductRepository:

    async def init(self):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Product:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, product) -> Product:
        raise NotImplementedError()