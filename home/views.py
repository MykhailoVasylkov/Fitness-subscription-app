from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from django.contrib import messages
from .models import NewsletterSubscriber


# Create your views here.

from django.contrib import messages
from .models import NewsletterSubscriber
from .forms import NewsletterSignupForm

def index(request):
    """
    A view to return the index page and collect subscription emails
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                subscriber = NewsletterSubscriber.objects.get(email=email)
                if subscriber.is_active:
                    messages.info(request, 'You are already subscribed to our newsletter.')
                else:
                    subscriber.is_active = True
                    subscriber.save()
                    messages.success(request, 'You have been re-subscribed to the newsletter.')
            except NewsletterSubscriber.DoesNotExist:
                # New email, create a subscriber
                NewsletterSubscriber.objects.create(email=email, is_active=True)
                messages.success(request, 'Thank you for subscribing!')

            return redirect('home')
    else:
        form = NewsletterSignupForm()

    return render(request, 'home/index.html', {'form': form})


def terms(request):
     """ A view to return the terms of use page """
     
     return render(request, 'home/terms_of_use.html')

def privacy(request):
     """ A view to return the privacy policy page """
     
     return render(request, 'home/privacy_policy.html')