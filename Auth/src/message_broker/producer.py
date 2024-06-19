from aiokafka import AIOKafkaProducer
from functools import lru_cache
import pickle

from Auth.src.config import get_config

app_config = get_config()

class Producer:
    def __init__(self) -> None:
        self.producer: AIOKafkaProducer = AIOKafkaProducer(bootstrap_servers=f'{app_config.Kafka.KAFKA_HOST}:{app_config.Kafka.KAFKA_PORT}')
        self.topic = app_config.Kafka.PRODUCER_TOPIC_VIEWS
    
    async def send_message(self, msg, topic):
        data = pickle.dumps(msg)
        await self.producer.send(topic=topic, value=data)
    
    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()


@lru_cache
def get_producer() -> Producer:
    return Producer() 
