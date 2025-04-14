import logging
from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated

from products.kafka import send_product_created_event
from products.models import Product
from products.serializers import ProductSerializer

logger = logging.getLogger(__name__)

__all__ = [
    "ProductsListAPIView",
    "ProductDetailAPIView",
]


class ProductsListAPIView(APIView):
    """
    API endpoint for listing all products and creating a new product.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_summary="List all products",
        responses={200: ProductSerializer(many=True)},
        tags=["Products"]
    )
    def get(self, request):
        """
        Returns a list of all available products.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        logger.info("Fetched all products")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
    operation_summary="Create a new product",
    request_body=ProductSerializer,
    responses={201: ProductSerializer},
    tags=["Products"]
    )
    def post(self, request):
        """
        Creates a new product with provided data and sends Kafka event.
        """

        if request.user.user_type != "seller":
            return Response({"detail": "Only sellers can create products."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(user_id=request.user.id)

            try:
                send_product_created_event({
                    "name": product.name,
                    "price": str(product.price),
                    "stock": product.stock,
                    "status": product.status,
                    "user_id": product.user_id,
                    "create_at": product.create_at.isoformat()
                })
            except Exception as e:
                logger.error(f"Kafka event failed: {e}")

            logger.info(f"Created new product: {product.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning("Failed to create product due to validation error")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class ProductDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating, or deleting a specific product.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a single product by ID",
        responses={200: ProductSerializer, 404: "Not Found"},
        tags=["Products"]
    )
    def get(self, request, product_id):
        """
        Retrieves the details of a specific product by its ID.
        """
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        logger.info(f"Retrieved product ID: {product_id}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a product by ID (partial)",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Bad Request", 404: "Not Found"},
        tags=["Products"]
    )
    def put(self, request, product_id):
        """
        Updates a product with new data. Allows partial updates.
        """
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Updated product ID: {product_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Failed to update product ID: {product_id}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a product by ID",
        responses={204: "No Content", 404: "Not Found"},
        tags=["Products"]
    )
    def delete(self, request, product_id):
        """
        Deletes the specified product.
        """
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        logger.info(f"Deleted product ID: {product_id}")
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
