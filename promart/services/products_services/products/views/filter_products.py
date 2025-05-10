from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.documents import  get_filtered_products


class ProductFilterAPIView(APIView):
    def get(self, request):
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        
        try:
            min_price = float(min_price) if min_price else None
            max_price = float(max_price) if max_price else None
            products = get_filtered_products(min_price, max_price)
            return Response({'products': products}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid price format'}, status=status.HTTP_400_BAD_REQUEST)