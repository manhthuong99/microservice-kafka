import json
import importlib

from kink import inject
from ...domain.repositories.product_repository import ProductRepository
from core.modules.message_module.message import MessageInterface
from loguru import logger


@inject
class ProductRepositoryImpl(ProductRepository):

    def __init__(self, message_queue: MessageInterface):
        self.message_queue = message_queue

    async def init(self):
        await self.message_queue.subscribe('catalog_product_save', self.handle_message)

    async def get_by_id(self, id: int):
        return {
            "id": 123,
            "name": "TEST",
            "sku": "TEST2"
        }

    async def save(self, product):
        data = json.dumps(product)
        await self.message_queue.send(topic="catalog_product_save", data=data)
        return True

    async def handle_message(self, topic, value):
        file_name = f"app.catalog.adapters.gateways.magento2.events.{topic}"
        try:
            module = importlib.import_module(file_name)
            process_function = getattr(module, "execute")
            logger.info(f"Process topic: {topic}")
            await process_function(value)
            logger.info(f"Process done: {topic}")

        except ImportError:
            logger.error(f"Failed to import module {file_name}")
        except AttributeError:
            logger.error(f"Module {file_name} does not contain the process function")
