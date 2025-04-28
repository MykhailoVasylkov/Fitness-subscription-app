from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order
from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    # chris made a mistake here, this function should have 
    # been called update_on_delete. He fixes this in an upcoming video.
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, created, **kwargs):
    if not created:
        # Check that the status has changed to the desired value
        if instance.status == 'shipped':
            cust_email = instance.email
            subject = render_to_string(
                'checkout/confirmation_emails/shipped_order_confirmation_email_subject.txt',
                {'order': instance})
            body = render_to_string(
                'checkout/confirmation_emails/shipped_order_confirmation_email_body.txt',
                {'order': instance, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )

        if instance.status == 'completed':
            cust_email = instance.email
            subject = render_to_string(
                'checkout/confirmation_emails/completed_order_confirmation_email_subject.txt',
                {'order': instance})
            body = render_to_string(
                'checkout/confirmation_emails/completed_order_confirmation_email_body.txt',
                {'order': instance, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )