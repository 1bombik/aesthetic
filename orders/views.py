from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from django.core.mail import send_mail
from django.conf import settings


def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})


def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.save()

        product_info = f'{order.product.title} - {order.quantity}'
        subject = 'Подтверждение заказа'
        message = f'Спасибо за заказ!. Ваш номер заказа - {order.id}.\n\nТовары:\n{product_info}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return redirect('orders:list')
    return render(request, 'orders/form.html', {'form': form})


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:list')
    return render(request, 'orders/delete.html', {'order': order})
