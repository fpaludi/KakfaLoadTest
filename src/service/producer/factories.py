import orjson
from dependency_injector import providers
from kafka import KafkaProducer

from service.producer.kafka_events_producer import KafkaEventsProducer
from settings import settings

kafka_producer_factory = providers.Factory(
    KafkaProducer,
    bootstrap_servers=settings.BROKER_URL.url,
    max_block_ms=10,
    value_serializer=lambda value: orjson.dumps(value),
)

producer_factory = providers.Factory(
    KafkaEventsProducer,
    kafka_producer_factory,
    topic=settings.WRITE_TOPIC,
)
