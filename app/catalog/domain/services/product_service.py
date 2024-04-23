from typing import Any, Coroutine

from .base_service import BaseService
from ...domain.entities.product import Product


class ProductService(BaseService):

    def __init__(self) -> None:
        super().__init__()

    def get_by_id(self, id: int) -> Coroutine[Any, Any, Product]:
        return self.product_repository.get_by_id(id)

    def save(self, product: dict):
        return self.product_repository.save(product)
