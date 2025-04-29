from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=[
        ('exercises', 'Exercises'),
        ('nutrition', 'Nutrition'),
    ])
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.PositiveIntegerField(default=1)
    plan_content = models.JSONField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    next_plan = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name