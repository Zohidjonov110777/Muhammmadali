from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True) # Filtrlash uchun shart!

    class Meta:
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    price = models.DecimalField(max_digits=12, decimal_places=0)
    old_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    label = models.CharField(max_length=10, choices=(('new','Yangi'),('sale','Chegirma')), null=True, blank=True)
    available = models.BooleanField(default=True)

    # Templatedagi 'subtract' xatosini yo'qotish uchun funksiya
    def get_discount_amount(self):
        if self.old_price and self.old_price > self.price:
            return self.old_price - self.price
        return 0

    def __str__(self): return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10) 
    color = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.product.name} - {self.size}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self): return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"