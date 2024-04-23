from .base_service import BaseService


class PromotionService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def save(self, promotion: dict):
        return self.promotion_repository.save(promotion)

    def apply(self, coupon):
        return self.promotion_repository.apply(coupon)
