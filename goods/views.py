from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .models import Product, Cart, CartItem, Order, OrderItem


def all_products(request):
    products = Product.objects.all()
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(id=product_id)
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            try:
                item = cart.items.get(product=product)
                item.quantity += quantity
                item.save()
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity,
                )
        else:
            cart = request.session.get('cart', {})
            cart_item = cart.get(str(product_id))
            if cart_item:
                cart_item['quantity'] += quantity
            else:
                cart_item = {'quantity': quantity}
            cart[str(product_id)] = cart_item
            request.session['cart'] = cart
        return redirect('cart')
    context = {'products': products}
    return render(request, 'goods/products.html', context)


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'goods/cart.html', {'items': cart_items, 'total_price': total_price})


def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_items.delete()
    return redirect('cart')


@login_required
@transaction.atomic
def checkout(request):
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        cart = request.session.get('cart')
        if cart is None:
            return redirect('cart')

    order = Order.objects.create(user=user if user.is_authenticated else None)

    order_items = []
    for item in cart.items.all():
        try:
            quantity = cart.items.through.objects.get(product=item, cart=cart).quantity
            if item.available_units < quantity:
                raise Exception(f'{item} не хватает на остатках. Актуальный остаток - {item.available_units}')
            order_item = OrderItem.objects.create(product=item, quantity=quantity, order=order)
            order_items.append(order_item)
        except Exception as e:
            transaction.set_rollback(True)
            return HttpResponseBadRequest(str(e))

    order_items = OrderItem.objects.filter(order=order)
    order.items.set([order_item.product for order_item in order_items])

    if not created:
        cart.items.clear()
    else:
        del request.session['cart']

    product_info = ''
    for order_item in order_items:
        product_info += f'{order_item.product.title} - {order_item.quantity}\n'

    subject = 'Подтверждение заказа'
    message = f'Спасибо за заказ! Ваш номер заказа - {order.id}.\n\nТовары:\n{product_info}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return redirect('cart')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    if request.method == 'POST':
        for item in cart_items:
            quantity = request.POST.get(f"quantity_{item.id}")
            if quantity is None:
                quantity = 0
            item.quantity = int(quantity)
            item.save()
        cart.save()
        return redirect('cart')
    else:
        return render(request, 'goods/cart.html', {'items': cart.items.all(), 'total_price': cart.total_price})
