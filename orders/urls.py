from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('delete/<int:order_id>/', views.order_delete, name='delete'),
]
