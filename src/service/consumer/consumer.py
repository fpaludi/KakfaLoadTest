import abc
from typing import Dict, List


class Consumer(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        """Connect consumer to broker"""
        pass

    @abc.abstractmethod
    def disconnect(self):
        """Disconnect consumer from broker"""
        pass

    @abc.abstractmethod
    def read_events(self) -> List[Dict]:
        """Gets events from broker"""
        pass
