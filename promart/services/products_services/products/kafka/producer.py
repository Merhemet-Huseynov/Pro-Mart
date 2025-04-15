import json
import logging
from kafka import KafkaProducer
from typing import Any, Dict, Optional

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Singleton producer instance
_producer: Optional[KafkaProducer] = None


def get_producer() -> KafkaProducer:
    """
    Lazily initialize and return a KafkaProducer instance.

    Returns:
        KafkaProducer: A singleton Kafka producer instance configured 
        to serialize JSON values.
    """
    global _producer
    if _producer is None:
        logger.info("Creating new Kafka producer...")
        _producer = KafkaProducer(
                  bootstrap_servers=["kafka:9092"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        logger.info("Kafka producer created successfully.")
    return _producer

def send_product_created_event(data: Dict[str, Any]):
    """
    Send a product_created event to the Kafka topic.

    Args:
        data (Dict[str, Any]): The event payload to be sent to Kafka.

    Returns:
        FutureRecordMetadata: A future that resolves to the record metadata once 
        the message is acknowledged.
    """
    logger.info("Sending product_created event with data: %s", data)
    future = get_producer().send("product_created", data)
    logger.info("Event sent to topic \"product_created\"")
    return future
