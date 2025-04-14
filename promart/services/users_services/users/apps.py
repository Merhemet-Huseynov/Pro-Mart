from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
<<<<<<< HEAD

    def ready(self):
        from users.kafka.consumer import start_consumer
        start_consumer()
=======
>>>>>>> 0fcf8c5f75a945c84a88977ec1336a8f80e94c41
