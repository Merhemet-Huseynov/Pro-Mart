from kafka import KafkaConsumer, errors
import json
import threading
import time
from users.models import CustomUser
from django.db.utils import IntegrityError

all = [
    "consume_product_created",
    "start_consumer"
]

def consume_product_created():
    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            consumer = KafkaConsumer(
                "product_created",
                bootstrap_servers="kafka:9092",
                auto_offset_reset="earliest",
                group_id="user-service-group",
                value_deserializer=lambda m: json.loads(m.decode("utf-8"))
            )
            break
        except errors.NoBrokersAvailable:
            time.sleep(retry_delay)
    else:
        return

    for message in consumer:
        data = message.value
        user_id = data.get("user_id")
        email = f"user{user_id}@gmail.com"

        try:
            CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            try:
                CustomUser.objects.create(
                    id=user_id,
                    email=email,
                    user_type="seller"
                )
            except IntegrityError:
                pass

def start_consumer():
    thread = threading.Thread(target=consume_product_created)
    thread.daemon = True
    thread.start()