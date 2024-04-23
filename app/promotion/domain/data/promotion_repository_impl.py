import json
import importlib

from fastapi.responses import JSONResponse
from kink import inject
from ...domain.repositories.promotion_repository import PromotionRepository
from core.modules.message_module.message import MessageInterface
from loguru import logger
from ..data.redis_module_singleton import RedisModuleSingleton
from ..data.odoo_api_singleton import Odoo2ApiSingleton


@inject
class PromotionRepositoryImpl(PromotionRepository):

    def __init__(self, message_queue: MessageInterface):
        self.message_queue = message_queue

    async def init(self):
        await self.message_queue.subscribe('promotion_save', self.handle_message)

    async def save(self, promotion):
        data = json.dumps(promotion)
        await self.message_queue.send(topic="promotion_save", data=data)
        return True

    async def handle_message(self, topic, value):
        file_name = f"app.promotion.domain.events.{topic}"
        module = importlib.import_module(file_name)
        process_function = getattr(module, "execute")
        logger.success(f"Value: {value}")
        await process_function(value)
        logger.success(f"[KAFKA MODULE] Processed {topic} - DONE!")

    async def apply(self, coupon):
        redis = RedisModuleSingleton.get_instance()
        coupon_data = await redis.get_cache(coupon)
        if not coupon_data:
            coupon_data = await self.get(coupon)

        can_apply_coupon = await self.can_apply_coupon(coupon_data)
        if not can_apply_coupon:
            content = {
                "message": "The coupon code isn't valid. Verify the code and try again."
            }
            return JSONResponse(content=content, status_code=404)
        return True

    async def can_apply_coupon(self, coupon_data):
        if not coupon_data.get('active'):
            return False

        if coupon_data.get('maximum_use_number') == 0:
            return True

        maximum_use_number = coupon_data.get('maximum_use_number')
        total_order_count = coupon_data.get('total_order_count')
        if total_order_count + 1 > maximum_use_number:
            return False

        return True

    async def get(self, coupon):
        coupon_data = {}
        odoo_api = Odoo2ApiSingleton.get_instance()
        params = {
            "promo_code": coupon
        }
        response = await odoo_api.do_request(endpoint="coupon_program", params=params)
        if response.get('status'):
            response_data = response.get('data')
            coupons = response_data.get('result').get('data')
            if len(coupons):
                coupon_data = coupons[0]

        return coupon_data
