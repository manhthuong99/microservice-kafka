import os
from kink import di

from .domain.repositories.product_repository import ProductRepository
from .adapters.repositories.product_repository_impl import ProductRepositoryImpl
from core.modules.message_module.message import MessageInterface
from core.modules.message_module.confluent_kafka.kafka_message import KafkaMessage


async def init_di():
    config = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
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

    product_repository = ProductRepositoryImpl()
    di[ProductRepository] = product_repository
    await product_repository.init()
