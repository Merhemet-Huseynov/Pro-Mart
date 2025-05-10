from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models.products_models import Product

product_index = Index('products')
product_index.settings(
    number_of_shards=1,
    number_of_replicas=1
)

@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(analyzer='standard')
    description = fields.TextField(analyzer='standard')
    price = fields.FloatField()
    stock = fields.IntegerField() 

    class Index:
        name = 'products'

    class Django:
        model = Product
        fields = [
            'id',
        ]


def get_filtered_products(min_price=None, max_price=None, product_name=None):
    
    search = ProductDocument.search()
    if min_price is not None and max_price is not None:
        search = search.filter('range', price={'gte': min_price, 'lte': max_price})
    elif min_price is not None:
        search = search.filter('range', price={'gte': min_price})
    elif max_price is not None:
        search = search.filter('range', price={'lte': max_price})
        
    # Product name filtering
    if product_name:
        search = search.query('match', name={'query': product_name, 'operator': 'and'})

    
    results = search.execute()
    products = [
        {
            'id': hit.id,
            'name': hit.name,
            'description': hit.description,
            'price': hit.price,
            'stock': hit.stock
        } for hit in results
    ]
    return products