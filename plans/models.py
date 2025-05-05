from django.db import models


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=[
        ('exercises', 'Exercises'),
        ('nutrition', 'Nutrition'),
    ])
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_weeks = models.PositiveIntegerField(default=1)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    level = models.IntegerField(choices=[
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Pro'),
    ])
    next_plan = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Week(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, related_name="weeks", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

class Day(models.Model):
    week = models.ForeignKey(Week, related_name="days", on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'), ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
        ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday'),
    ])

class DayContentItem(models.Model):
    day = models.ForeignKey(Day, related_name="content_items", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.TextField()  
