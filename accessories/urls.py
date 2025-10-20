from django.urls import path
from . import views

# App name for namespacing URLs
app_name = 'accessories'

urlpatterns = [
    # URL: /accessories/products/
    path('products/', views.products, name='products'),

    # URL: /accessories/search/
    path('search/', views.product_search, name='product_search'),

    # URL: /accessories/add-to-cart/1/
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # URL: /accessories/cart/
    path('cart/', views.cart, name='cart'),

    # URL: /accessories/update-cart/1/
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),

    # URL: /accessories/remove-from-cart/1/
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # URL: /accessories/checkout/
    path('checkout/', views.checkout, name='checkout'),
]