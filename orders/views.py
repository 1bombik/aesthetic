from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from goods.models import OrderItem


def order_list(request):
    orders = OrderItem.objects.filter(order__user=request.user)
    orders_manually = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders,
                                                'orders_manually': orders_manually})
