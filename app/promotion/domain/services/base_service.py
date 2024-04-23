from kink import inject
from ...domain.repositories.promotion_repository import PromotionRepository


@inject
class BaseService:
    def __init__(self, promotion_repository: PromotionRepository) -> None:
        self.promotion_repository = promotion_repository
