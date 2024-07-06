# models.py

from django.db import models
from django.contrib.auth.models import User
from .validators import CustomImageField  # Ensure this import is correct

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username  # Ensure this returns the username

class Product(models.Model):
    product_image = CustomImageField(upload_to="products/")
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_logo = CustomImageField(upload_to="products/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.product_name

class PlatformImages(models.Model):
    short_images = CustomImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='platform_images')

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_features')
    product_features_count = models.CharField(max_length=50)
    product_features_items = models.CharField(max_length=200)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"