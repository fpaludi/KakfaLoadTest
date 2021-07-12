import time
from kafka.errors import NoBrokersAvailable

from service.logger import configure_logger, get_logger
from service.producer import producer_factory, Producer
from service.consumer import consumer_factory, Consumer
from settings import settings


def main():
    configure_logger()
    logger = get_logger("MAIN")
    connected = False

    while not connected:
        try:
            consumer: Consumer = consumer_factory()
            producer: Producer = producer_factory()
            connected = True
        except NoBrokersAvailable:
            connected = False
            logger.warning("Trying to connect")

    consumer.connect()
    producer.connect()
    logger.info("Start")
    try:
        while True:
            events = consumer.read_events()
            for event in events:
                producer.send_event(event)
                logger.info("Sending")
                time.sleep(settings.SLEEP_TIME_S)
    finally:
        consumer.disconnect()
        producer.disconnect()
        logger.info("Finish")

if __name__ == "__main__":
    main()
