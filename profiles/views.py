from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Achievement
from .models import UserProfile
from checkout.models import Order, Subscription
from .forms import UserProfileForm

import json

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    subscriptions = profile.subscriptions.all()

    # Create achievements library for checking already existing items in the template
    achievements = Achievement.objects.filter(user=request.user).values(
        "plan_name", "week_number", "day_name", "content_item"
    )

    completed_tokens = []
    for a in achievements:
        token = f"{a['plan_name']}|{a['week_number']}|{a['day_name']}|{a['content_item']}"
        completed_tokens.append(token)

    completed_tokens_json = json.dumps(completed_tokens, cls=DjangoJSONEncoder)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'subscriptions': subscriptions,
        'on_profile_page': True,
        'completed_tokens_json': completed_tokens_json,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

def plan_order_history(request, subscription_number):
    subscription = get_object_or_404(Subscription, subscription_number=subscription_number)

    messages.info(request, (
        f'This is a past confirmation for order number {subscription_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'subscription': subscription,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def save_achievement(request):
    if request.method == "POST":
        user = request.user
        plan_name = request.POST.get("plan_name")
        week_number = request.POST.get("week_number")
        day_name = request.POST.get("day_name")
        content_item = request.POST.get("content_key")
        checked = request.POST.get("checked") == 'true'

        if checked:
            # If cheked - add
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                plan_name=plan_name,
                week_number=week_number,
                day_name=day_name,
                content_item=content_item
            )
        else:
            # If removed - delete
            Achievement.objects.filter(
                user=user,
                plan_name=plan_name,
                week_number=week_number,
                day_name=day_name,
                content_item=content_item
            ).delete()

        return JsonResponse({"success": True})
