from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, BaseSettings, confloat, validator


class LogLevelEnum(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"

class KafkaURL(BaseModel):
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(BaseSettings):
    CONSUMER_GROUP: str = "1234567890"

    # Kafka
    BROKER_HOST: str = "message-broker"
    BROKER_PORT: int = 9092
    BROKER_URL: Optional[KafkaURL] = None
    READ_TOPIC: str = "read.events"
    WRITE_TOPIC: str = "write.events"
    SLEEP_TIME_S: float = 1

    # Logger
    LOG_LEVEL = LogLevelEnum.info
    LOG_FILE = "log_file.log"

    @validator("BROKER_URL", pre=True)
    def assemble_kafka_url(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> KafkaURL:
        return KafkaURL(
            host=values.get("BROKER_HOST"),
            port=values.get("BROKER_PORT"),
        )

    class Config:
        use_enum_values = True


settings = Settings()
