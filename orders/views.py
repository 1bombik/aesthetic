from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from goods.models import OrderItem


def order_list(request):
    orders = OrderItem.objects.filter(order__user=request.user)
    orders_manually = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders,
                                                'orders_manually': orders_manually})


def order_delete(request, order_id):
    order = get_object_or_404(OrderItem, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:list')
    return render(request, 'orders/delete.html', {'order': order})
