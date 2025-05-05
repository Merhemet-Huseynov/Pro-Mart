from django.urls import path

from products.views import *

urlpatterns = [
    # Product endpoints
    path(
        "products",
        ProductsListAPIView.as_view(),
        name="products-list"
    ),

    path(
        "products/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail"
    ),
    
    # Category endpoints
    path(
        "categories/",
        SuperCategoryAPIView.as_view(),
        name="category-list"
    ),
    
    path(
        "subcategories/<int:super_id>/",
        SubCategoryAPIView.as_view(),
        name="subcategory-list"
    ),
]

