import asyncio
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from loguru import logger

from core.modules.message_module.message import MessageInterface


class KafkaMessage(MessageInterface):

    def __init__(self, admin_cfg, producer_cfg, consumer_cfg, *args, **kwargs):
        self.handlers = {}
        self.admin_cfg = admin_cfg
        self.producer_cfg = producer_cfg
        self.consumer_cfg = consumer_cfg

    async def init(self):
        self.admin = AdminClient(self.admin_cfg)
        self.producer = Producer(self.producer_cfg)
        self.consumer = Consumer(self.consumer_cfg)
        asyncio.get_event_loop().create_task(self._get_messages())

    async def _get_messages(self):
        try:
            while True:
                await asyncio.sleep(0.1)
                messages = self.consumer.consume(10, 0.01)
                if len(messages) == 0:
                    continue
                logger.info(f'[KAFKA MODULE] Received {len(messages)} message')
                for message in messages:
                    topic = message.topic()
                    value = message.value()
                    value = value.decode('utf8')
                    if topic in self.handlers:
                        futures = []
                        if self.handlers[topic]:
                            callback = self.handlers[topic]
                            futures.append(callback(topic, value))
                        if len(futures) > 0:
                            logger.info(f'[KAFKA MODULE] Processing topic {topic}')
                            await asyncio.gather(*futures)

        except Exception as ex:
            logger.exception(str(ex), ex)

    async def create_topics(self, topic, num_partition=5, replication_factor=1):
        lst_topic = [NewTopic(topic, num_partition, replication_factor)]
        logger.info(f"[KAFKA MODULE] List topics for create: {lst_topic}")
        topics = self.admin.create_topics(lst_topic)
        logger.info(f"[KAFKA MODULE] Created topics: {lst_topic}")
        return topics

    async def send(self, topic, data, key=None, *args, **kwargs):
        try:
            self.producer.produce(topic, value=data)
        except Exception as ex:
            print("Producer Error :", ex)

    async def subscribe(self, topic, callback, *args, **kwargs):
        try:
            if self.admin.list_topics().topics.get(topic) is None:
                topics = await self.create_topics(topic)

            if not topic in self.handlers:
                self.handlers[topic] = {}

            self.handlers[topic] = callback
            self.consumer.subscribe([topic])
            logger.info(f"[KAFKA MODULE] Subscribed topic {topic}")

        except Exception as ex:
            logger.info(f"[KAFKA MODULE] Subscribe Error : {ex}")

    async def flush(self, *args, **kwargs):
        self.producer.flush()

    async def close(self):
        pass
