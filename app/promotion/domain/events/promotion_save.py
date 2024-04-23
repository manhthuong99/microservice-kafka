import json

from ..data.magento_api_singleton import Magento2ApiSingleton
from ..data.redis_module_singleton import RedisModuleSingleton
from loguru import logger

discount_type = {
    'percentage': 'by_percent'
}

coupon_type = {
    'percentage': 2
}


async def execute(data):
    m2_api = Magento2ApiSingleton.get_instance()
    if isinstance(data, str):
        data = json.loads(data)

    promotions = data.get('result').get('data')
    for promotion in promotions:
        params = await get_m2_promotion_data(promotion)
        logger.info("[PROMOTION_EVENTS] Update m2 promotion")
        response = await m2_api.do_request('saveSaleRules', params=json.dumps(params), method='POST')
        if response.get('status'):
            coupon = promotion.get("promo_code")
            redis = RedisModuleSingleton.get_instance()
            logger.info("[PROMOTION_EVENTS] save promotion to redis")
            await redis.set_cache(coupon, promotion)


async def get_m2_promotion_data(promotion):
    promotion_data = {
        "name": promotion.get("name"),
        "coupon_code": promotion.get("promo_code"),
        "uses_per_customer": 1,
        "sort_order": "",
        "discount_amount": promotion.get('discount_percentage'),
        "discount_qty": 0,
        "discount_step": "",
        "store_labels": {
            "0": promotion.get('display_name'),
            "1": ""
        },
        "description": "Test Discount 10%",
        "is_active": int(promotion.get('active')),
        "use_auto_generation": 0,
        "is_rss": 1,
        "stop_rules_processing": 1,
        "apply_to_shipping": 0,
        "from_date": promotion.get('rule_date_from'),
        "to_date": promotion.get('rule_date_to'),
        "simple_action": discount_type.get(promotion.get('discount_type')),
        "simple_free_shipping": "",
        "coupon_type": coupon_type.get(promotion.get('discount_type')),
        "website_ids": {
            "0": 1
        },
        "customer_group_ids": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3
        }
    }

    if promotion.get('maximum_use_number'):
        promotion_data['uses_per_coupon'] = promotion.get('maximum_use_number')

    return promotion_data
