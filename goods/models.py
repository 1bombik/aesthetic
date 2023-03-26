from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
