from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField

"""
Code snippet form Boutique Ado
"""


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text='Upload your image',
        default='avatars/default_avatar.jpg'
    )
    nickname = models.CharField(max_length=30, null=True, blank=True)
    full_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=True,
        null=True
    )
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )
    default_county = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    week_number = models.IntegerField()
    day_name = models.CharField(max_length=255)
    content_item = models.CharField(max_length=255)
    date_completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} - {self.plan_name} - "
            f"Week {self.week_number} - {self.day_name} - {self.content_item}"
        )
