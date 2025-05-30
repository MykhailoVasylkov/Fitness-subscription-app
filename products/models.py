from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


"""
I used Boutique Ado project and project #4 code.
Category model with name and friendly name fields.
"""


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


"""
I used Boutique Ado project and project #4 code.
Product model represents a product item in a shop's system.
"""


class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    brand = models.ForeignKey(
        'Brand',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available'
    )

    def __str__(self):
        return self.name


"""
ProductSize model represents a sizes for a linked product.
"""


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('3XL', '3XL'),
        ('4XL', '4XL'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes'
    )
    size = models.CharField(
        max_length=4,
        choices=SIZE_CHOICES,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


"""
Brand model represents a brand for a linked product.
"""


class Brand(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


"""
Product Review model for storing user reviews with rating (1-5),
body, approval status, and timestamps.
"""


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product_reviews",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating must be between 1 and 5"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Review by {self.author.username} - {self.rating}⭐"
