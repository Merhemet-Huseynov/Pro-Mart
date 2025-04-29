import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import asyncio

from products.models import Product
from products.serializers import ProductSerializer
from utils.permissions import is_seller
from utils.telegram_sender import send_product_to_telegram
from products.kafka.producer import send_message


logger = logging.getLogger(__name__)

__all__ = ["ProductsListAPIView", "ProductDetailAPIView"]

class ProductsListAPIView(APIView):
    """
    API endpoint for listing all products and creating a new product.
    
    This view allows authenticated users to view all products, and sellers to create new products.
    The 'GET' method is accessible by anyone, while the 'POST' method is restricted to sellers.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the HTTP method.
        
        'GET' requests are accessible by anyone, while 'POST' requests require the user to be authenticated.
        """
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Returns a list of all available products.",
        responses={200: openapi.Response(
            description="Successful operation",
            schema=ProductSerializer(many=True)
        )}
    )
    def get(self, request):
        """
        Retrieves and returns a list of all products in the system.
        
        This method is accessible by anyone.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Allows sellers to create new products. Only users with 'seller' user_type can perform this action.",
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Product successfully created",
                schema=ProductSerializer()
            ),
            400: "Bad request",
            403: "Forbidden - Only sellers can create products",
        }
    )
    def post(self, request):
        """
        Creates a new product in the system.
        This method is restricted to authenticated users with 'seller' user_type.
        """
        user_id = request.user.id

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(user_id=user_id)
            logger.info(f"Yeni məhsul yaradıldı: {product.name} (user_id={user_id})")
            
            # Kafka-ya göndərmək üçün dictionary düzəldirik
            message_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock": product.stock,
                "status": product.status,
                "user_id": product.user_id,
                "image": product.image.url if product.image else None,
            }

            # 'id' key olaraq, 'name' isə value olaraq Kafka-ya göndərilir
            send_message("product_topic", str(product.id), str(product.name))
            
            # Teleqram bildirişi
            asyncio.run(send_product_to_telegram(product))
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning("Məhsul yaratmaq uğursuz oldu: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific product.
    
    This view provides access to detailed operations for a single product:
    - 'GET': Retrieve product details.
    - 'PUT': Update product information.
    - 'DELETE': Delete a product from the system.
    """
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Returns the appropriate permissions based on the HTTP method.
        
        'GET' requests are accessible by anyone, while 'PUT' and 'DELETE' requests require the user to be authenticated.
        """
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, product_id):
        """
        Retrieves and returns the details of a specific product by its ID.
        
        This method is accessible by anyone.
        """
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        """
        Updates the details of a specific product by its ID.
        
        This method is only accessible by authenticated users.
        """
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """
        Deletes a specific product from the system by its ID.
        
        This method is only accessible by authenticated users.
        """
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
