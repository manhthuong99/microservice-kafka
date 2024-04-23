import os
from kink import di
from loguru import logger

from .domain.repositories.promotion_repository import PromotionRepository
from .domain.data.promotion_repository_impl import PromotionRepositoryImpl
from core.modules.message_module.message import MessageInterface
from core.modules.message_module.confluent_kafka.kafka_message import KafkaMessage
from .domain.data.magento_api_singleton import Magento2ApiSingleton
from .domain.data.redis_module_singleton import RedisModuleSingleton
from .domain.data.odoo_api_singleton import Odoo2ApiSingleton


async def init_di():
    # Init Kafka
    config = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:29092'),
        'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
    }
    admin_cfg = {}
    producer_cfg = {}
    consumer_cfg = {
        'auto.offset.reset': 'earliest',
        'group.id': 'grp1'
    }
    admin_cfg.update(config)
    producer_cfg.update(config)
    consumer_cfg.update(config)

    kafka_message = KafkaMessage(admin_cfg=admin_cfg, producer_cfg=producer_cfg, consumer_cfg=consumer_cfg)
    di[MessageInterface] = kafka_message
    await kafka_message.init()
    logger.info("Initialized Kafka")

    # Init Promotion Repository
    promotion_repository = PromotionRepositoryImpl()
    di[PromotionRepository] = promotion_repository
    await promotion_repository.init()
    logger.info("Initialized Promotion Repository")

    # Init Redis
    redis_module = RedisModuleSingleton.get_instance()
    await redis_module.init(
        redis_host=os.getenv("REDIS_HOST"),
        redis_port=os.getenv("REDIS_PORT"),
        redis_db=os.getenv("REDIS_DB")
    )
    logger.info("Initialized Redis")

    # Init M2 APIs
    m2_api = Magento2ApiSingleton.get_instance()
    await m2_api.init(
        base_url=os.getenv('M2_BASE_URL'),
        bearer_token=os.getenv('M2_BEARER_TOKEN'),
        api_version=os.getenv('M2_API_VERSION'),
        store='default'
    )
    logger.info("Initialized M2 APIs")

    # Init Odoo APIs
    odoo_api = Odoo2ApiSingleton.get_instance()
    await odoo_api.init(
        base_url=os.getenv('ODOO_BASE_URL'),
        access_token=os.getenv('ODOO_ACCESS_TOKEN')
    )
    logger.info("Initialized Odoo APIs")
