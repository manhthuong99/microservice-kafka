from kink import inject
from ...domain.repositories.product_repository import ProductRepository


@inject
class BaseService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository
