from django.db import models
from users.models import CustomUser


class Product(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available_units = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_cart_item_count(self, user):
        if user.is_authenticated:
            cart = user.cart
            try:
                item = cart.items.get(product=self)
                return item.quantity
            except CartItem.DoesNotExist:
                return 0
        else:
            return 0


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    items = models.ManyToManyField(Product, through='OrderItem', related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Заказ {self.order.id}"
