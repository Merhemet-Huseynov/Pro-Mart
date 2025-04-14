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
            print("✅ \"product_created\" mövzusuna qulaq asılır...")
            break
        except errors.NoBrokersAvailable:
            print(f"❌ Kafka hələ mövcud deyil. Təkrar cəhd {attempt + 1}/{max_retries}...")
            time.sleep(retry_delay)
    else:
        print("🔥 Kafka əlaqəsi cəhdlərdən sonra uğursuz oldu.")
        return

    for message in consumer:
        data = message.value
        print("🔔 Yeni mesaj alındı:", data)

        user_id = data.get("user_id")
        email = f"user{user_id}@gmail.com"

        try:
            CustomUser.objects.get(id=user_id)
            print(f"🔎 ID {user_id} olan istifadəçi artıq mövcuddur.")
        except CustomUser.DoesNotExist:
            try:
                CustomUser.objects.create(
                    id=user_id,
                    email=email,
                    user_type="seller"
                )
                print(f"✅ ID {user_id} olan istifadəçi yaradıldı.")
            except IntegrityError:
                print(f"⚠️ IntegrityError: ID {user_id} olan istifadəçi artıq mövcuddur")

def start_consumer():
    thread = threading.Thread(target=consume_product_created)
    thread.daemon = True
    thread.start()
