# from ..kafka.producer import KafkaProducerMessage
import logging
import json


logging.basicConfig(filename="app/catalog/var/log/debug.log")


class ProductGateway:
    PRODUCT_ENDPOINT = "products"

    def __int__(self):
        pass
        # super().__init__({"store": "default"})

    def update_product(self, product):
        data = json.dumps(product)
        logging.info(f"Message pushed: {product}")
        # kafka_producer.send_message(product)
        return {"success": True}
