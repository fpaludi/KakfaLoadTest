import abc
from typing import Any, Dict, List, Union

JSONEvent = Union[Dict[str, Any], List[Any]]


class Producer(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        """Connect producer to broker"""
        pass

    @abc.abstractmethod
    def disconnect(self):
        """Disconnect producer from broker"""
        pass

    @abc.abstractmethod
    def send_event(self, event: JSONEvent):
        """Sends event to broker"""
        pass
