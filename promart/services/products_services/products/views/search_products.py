from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl.query import MultiMatch
from products.documents import ProductDocument

class ProductSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'error': 'Axtarış üçün sorğu (q) daxil edilməlidir.'}, status=status.HTTP_400_BAD_REQUEST)

        search_query = ProductDocument.search().query(
            MultiMatch(query=query, fields=['name', 'description'])
        )
        results = search_query.execute()
        data = [
            {
                'id': hit.id,
                'name': hit.name,
                'description': hit.description,
                'price': hit.price,
                'stock': hit.stock,
            }
            for hit in results
        ]
        return Response(data)
