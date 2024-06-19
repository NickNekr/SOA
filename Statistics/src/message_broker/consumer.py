from aiokafka import AIOKafkaConsumer
import pickle

from Statistics.src.config import get_config

app_config = get_config()

async def consume(topic, callback):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=f'{app_config.Kafka.KAFKA_HOST}:{app_config.Kafka.KAFKA_PORT}')
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, pickle.loads(msg.value), msg.timestamp)
            await callback(msg)
    except Exception as e:
        print(e)
    finally:
        print("Bye")
        await consumer.stop()
