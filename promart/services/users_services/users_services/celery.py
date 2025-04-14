from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings modulunu seçirik
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users_services.settings")

app = Celery("users_services")

# Celery konfiqurasiyasını Django'nun settings.py faylından alırıq
app.config_from_object("django.conf:settings", namespace="CELERY")

# Kafka brokeri istifadə etmək üçün broker_url təyin edirik
app.conf.update(
    broker_url='kafka://kafka:9092',  # Kafka'nın URL-ini burada təyin edirik
    task_serializer='json',  # JSON formatında mesajları serializasiya edirik
    result_backend='rpc://',  # Kafka ilə nəticələri almaq üçün RPC backend istifadə edilə bilər
)

# Tapşırıqları avtomatik qeydiyyatdan keçiririk
app.autodiscover_tasks()
