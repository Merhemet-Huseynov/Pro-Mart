from kafka import KafkaProducer
import json
from typing import Any, Dict, Optional

_producer: Optional[KafkaProducer] = None

def get_kafka_producer() -> KafkaProducer:
    """
    Lazily initialize and return a KafkaProducer instance.

    Returns:
        KafkaProducer: The initialized Kafka producer.
    """
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=["kafka:9092"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    return _producer

def send_product_created_event(data: Dict[str, Any]) -> None:
    """
    Send a "product_created" event with the given data to the Kafka topic.

    Args:
        data (Dict[str, Any]): The product data to be sent as a message.
    """
    producer = get_kafka_producer()
    producer.send("product_created", data)
