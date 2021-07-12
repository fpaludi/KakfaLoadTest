from typing import Dict, List

from kafka import KafkaConsumer
from kafka.structs import TopicPartition

from service.consumer.consumer import Consumer
from service.logger import get_logger


class KafkaEventsConsumer(Consumer):
    """Class responsible of consuming events from Kafka broker"""

    def __init__(self, consumer: KafkaConsumer, topic: str):
        """Class constructor

        Parameters
        ----------
        consumer : KafkaConsumer
            Kafka consumer object
        topics : str
            Topic to consume from broker
        """
        self._consumer = consumer
        self._logger = get_logger(self.__class__.__name__)
        self._assign_partition(topic)

    def _assign_partition(self, topic: str):
        """Assign partition and start consuming from latest event

        Parameters
        ----------
        topics : str
            List of topics to consume from broker
        """
        partition_assigned = False
        while not partition_assigned:
            try:
                topic_partition = [
                    TopicPartition(topic, partition)
                    for partition in self._consumer.partitions_for_topic(topic)
                ]
                self._consumer.assign(topic_partition)
                self._consumer.seek_to_end(*topic_partition)
                partition_assigned = True
            except (TypeError) as excp:
                self._logger.warn("Trying to assign partition")
                self._logger.debug(
                    f"Assignment was not possible because of: {excp}"
                )

    def connect(self):
        """Connect to broker"""
        # Nothing to do here
        pass

    def disconnect(self):
        """Disconnect from broker"""
        self._consumer.close()

    def read_events(self) -> List[Dict]:
        """Gets events from broker"""
        events = [event.value for event in self._consumer]
        #events = [event for event in self._consumer.poll(100)[1:]]
        return events
