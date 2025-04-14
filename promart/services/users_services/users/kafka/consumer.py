from kafka import KafkaConsumer, errors
import json
import threading
import time
from users.models import CustomUser
from django.db.utils import IntegrityError

__all__ = [
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
            print("✅ Listening to \"product_created\" topic...")
            break
        except errors.NoBrokersAvailable:
            print(f"❌ Kafka not available yet. Retry {attempt + 1}/{max_retries}...")
            time.sleep(retry_delay)
    else:
        print("🔥 Kafka connection failed after retries.")
        return

    for message in consumer:
        data = message.value
        print("🔔 New message received:", data)

        user_id = data.get("user_id")
        email = f"user{user_id}@gmail.com"

        try:
            CustomUser.objects.get(id=user_id)
            print(f"🔎 User with ID {user_id} already exists.")
        except CustomUser.DoesNotExist:
            try:
                CustomUser.objects.create(
                    id=user_id,
                    email=email,
                    user_type="seller"
                )
                print(f"✅ Created user with ID {user_id}")
            except IntegrityError:
                print(f"⚠️ IntegrityError: User with ID {user_id} already exists")

def start_consumer():
    thread = threading.Thread(target=consume_product_created)
    thread.daemon = True
    thread.start()
Pro-Mart/promart/services/users_services/users/kafka/consumer.py