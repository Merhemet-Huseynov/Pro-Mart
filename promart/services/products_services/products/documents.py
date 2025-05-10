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
