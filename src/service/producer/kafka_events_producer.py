from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from service.logger import get_logger
from service.producer.producer import JSONEvent, Producer


class KafkaEventsProducer(Producer):
    def __init__(self, producer: KafkaProducer, topic: str):
        """Class constructor

        Parameters
        ----------
        producer : KafkaProducer
            Kafka producer object
        topic : str
            Topic where events are send
        """
        self._producer = producer
        self._topic = topic
        self._logger = get_logger(self.__class__.__name__)

    def connect(self):
        """Connect producer to broker"""
        # Nothing to do here
        pass

    def disconnect(self):
        """Disconnect producer from broker"""
        self._producer.close()

    def send_event(self, event: JSONEvent):
        """Sends event to broker
        Parameters
        ----------
        event : JSONEvent
            event data
        """
        try:
            self._producer.send(topic=self._topic, value=event)
            self._logger.debug("Send event", topic=self._topic, value=event)
        except KafkaTimeoutError:
            self._logger.error(
                "Unable to send message. Kafka producer Timeout"
            )
