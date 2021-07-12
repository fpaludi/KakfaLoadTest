from datetime import datetime
import uuid
import orjson
import gevent
from kafka import KafkaConsumer, TopicPartition
from locust_plugins import run_single_user
from locust_plugins.users import KafkaUser
from locust import task, between, events
from settings import settings


_DATA = {}

class MyUser(KafkaUser):
    bootstrap_servers = "localhost:9093" #settings.BROKER_URL.url
    wait_time = lambda x: 0.01 # between(0.01, 0.1)

    @task
    def t(self):
        self.client.send(settings.READ_TOPIC, orjson.dumps(self.get_payload()))
        # self.client.producer.poll(0.01)

    def get_payload(self):
        payload = {
            "timestamp": datetime.now(),
            "uuid": uuid.uuid4(),
            "data": {
                "field1": 10,
                "field2": 20
            }
        }
        global _DATA
        _DATA[str(payload["uuid"])] = payload["timestamp"]
        return payload

# How to set up a (global) consumer and read the last message. Consider this as inspiration, it might not work for you.
# And it is probably out of date. Probably best to ignore this.
#
@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    consumer = KafkaConsumer(
        bootstrap_servers=MyUser.bootstrap_servers,
        auto_offset_reset="latest",
        group_id="lalalalala",
        enable_auto_commit=True,
        value_deserializer=lambda value: orjson.loads(value),
    )
    tp = TopicPartition(settings.WRITE_TOPIC, 0)
    consumer.assign([tp])
    consumer.seek_to_end()
    gevent.spawn(wait_for_retrans, environment, consumer)

def wait_for_retrans(environment, consumer):
    for message in consumer:
        global _DATA
        dt = datetime.fromtimestamp(message.timestamp / 1000)
        send_time = _DATA.pop(str(message.value["uuid"]))
        response_time = (dt - send_time).microseconds / 1000

        environment.events.request_success.fire(
            request_type="CONSUME",
            name="retrans2",
            response_time=response_time,
            response_length=0,
        )

if __name__ == "__main__":
    run_single_user(MyUser)