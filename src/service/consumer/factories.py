import json

from dependency_injector import providers
from kafka import KafkaConsumer

from service.consumer.kafka_events_consumer import KafkaEventsConsumer
from settings import settings

kafka_consumer_factory = providers.Factory(
    KafkaConsumer,
    bootstrap_servers=settings.BROKER_URL.url,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id=settings.CONSUMER_GROUP,
    consumer_timeout_ms=10,
    #auto_commit_interval_ms=1000,
    value_deserializer=lambda value: json.loads(value),
)

consumer_factory = providers.Factory(
    KafkaEventsConsumer,
    kafka_consumer_factory,
    topic=settings.READ_TOPIC,
)
