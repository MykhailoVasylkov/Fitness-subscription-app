from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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
    
    def average_rating(self):
        return self.plan_reviews.filter(approved=True).aggregate(Avg('rating'))['rating__avg'] or 0
    

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


class SubscriptionPlanSnapshot(models.Model):
    original_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20)
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_weeks = models.PositiveIntegerField(default=1)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    snapshot_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Snapshot)"


class WeekSnapshot(models.Model):
    plan_snapshot = models.ForeignKey(SubscriptionPlanSnapshot, related_name="weeks", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()


class DaySnapshot(models.Model):
    week_snapshot = models.ForeignKey(WeekSnapshot, related_name="days", on_delete=models.CASCADE)
    name = models.CharField(max_length=10)


class DayContentItemSnapshot(models.Model):
    day_snapshot = models.ForeignKey(DaySnapshot, related_name="content_items", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.TextField()


def clone_plan(plan):
    # Create a copy of the plan
    plan_snapshot = SubscriptionPlanSnapshot.objects.create(
        original_plan=plan,
        name=plan.name,
        category=plan.category,
        description=plan.description,
        rating=plan.rating,
        price=plan.price,
        duration_weeks=plan.duration_weeks,
        image_url=plan.image_url,
        image=plan.image,
        level=plan.level
    )

    # Copy all weeks
    for week in plan.weeks.all():
        week_snapshot = WeekSnapshot.objects.create(
            plan_snapshot=plan_snapshot,
            number=week.number
        )

        # Copy all days
        for day in week.days.all():
            day_snapshot = DaySnapshot.objects.create(
                week_snapshot=week_snapshot,
                name=day.name
            )

            # Copy all content elements
            for content_item in day.content_items.all():
                DayContentItemSnapshot.objects.create(
                    day_snapshot=day_snapshot,
                    key=content_item.key,
                    value=content_item.value
                )

    return plan_snapshot

"""
Plan Review model for storing user reviews with rating (1-5),
body, approval status, and timestamps.
"""
class PlanReview(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, related_name="plan_reviews", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
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
