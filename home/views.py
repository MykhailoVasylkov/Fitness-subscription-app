from django.shortcuts import render, redirect, reverse
import uuid
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.conf import settings

from .forms import NewsletterSignupForm
from django.contrib import messages
from .models import NewsletterSubscriber


def index(request):
     """
     A view to return the index page and collect subscription emails with confirmation token.
     Used Chat-GPT
     """
     if request.method == 'POST':
          form = NewsletterSignupForm(request.POST)
          if form.is_valid():
               email = form.cleaned_data['email']
               try:
                    subscriber = NewsletterSubscriber.objects.get(email=email)
                    if subscriber.is_active:
                         messages.info(request, 'You are already subscribed to our newsletter.')
                         return redirect('home')
                    else:
                         # Inactive subscriber - need to send a new confirmation email
                         subscriber.unsubscribe_token = uuid.uuid4()
                         subscriber.confirmation_token = uuid.uuid4()
                         subscriber.is_active = False
                         subscriber.save()
               except NewsletterSubscriber.DoesNotExist:
                    # New subscriber
                    subscriber = NewsletterSubscriber.objects.create(
                    email=email,
                    is_active=False,
                    confirmation_token=uuid.uuid4()
                    )

               # We are sending a confirmation letter
               current_site = get_current_site(request)
               confirmation_link = request.build_absolute_uri(
                    reverse('confirm_subscription', args=[str(subscriber.confirmation_token)])
               )
               subject = 'Confirm your subscription'
               from_email = settings.DEFAULT_FROM_EMAIL
               to = [subscriber.email]

               context = {
                    'confirmation_link': confirmation_link,
                    'domain': current_site.domain,
                    'subscriber': subscriber,
               }

               html_content = render_to_string('emails/confirm_email_subscription.html', context)
               text_content = f'Please confirm your subscription by visiting: {confirmation_link}'

               email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
               email_msg.attach_alternative(html_content, "text/html")
               email_msg.send()

               messages.success(request, 'Please check your email to confirm your subscription.')
               return redirect('home')
     else:
          form = NewsletterSignupForm()

     return render(request, 'home/index.html', {'form': form})


def confirm_subscription(request, token):
     try:
          subscriber = NewsletterSubscriber.objects.get(confirmation_token=token)
          subscriber.is_active = True
          subscriber.save()
     except NewsletterSubscriber.DoesNotExist:
          subscriber = None

     unsubscribe_link = request.build_absolute_uri(
          reverse('unsubscribe', args=[str(subscriber.unsubscribe_token)])
)

     current_site = get_current_site(request)
     context = {
          'subscriber': subscriber,
          'unsubscribe_link': unsubscribe_link,
     }
     return render(request, 'home/confirm_subscription.html', context)


def unsubscribe(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, unsubscribe_token=token)

    if subscriber.is_active:
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, f'You have successfully unsubscribed from the newsletter.')
    else:
        messages.info(request, 'You are already unsubscribed.')

    return redirect('home')


def terms(request):
     """ A view to return the terms of use page """
     
     return render(request, 'home/terms_of_use.html')

def privacy(request):
     """ A view to return the privacy policy page """
     
     return render(request, 'home/privacy_policy.html')