from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = "__all__"
        read_only_fields = ['user_id']
=======
        fields = "__all__"
>>>>>>> 0fcf8c5f75a945c84a88977ec1336a8f80e94c41
