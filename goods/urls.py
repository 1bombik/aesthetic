from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all-products'),
    path('cart/', views.cart, name='cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),
]
