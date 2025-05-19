'''
Code snippet from Boutique Ado
'''
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum

from .forms import OrderForm, SubscriptionForm
from .models import Order, OrderLineItem, Subscription, SubscriptionLineItem
from plans.models import SubscriptionPlan, clone_plan
from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        # Get secrets of payment intentions
        product_pid = request.POST.get('product_client_secret', '').split('_secret')[0]
        subscription_pid = request.POST.get('subscription_client_secret', '').split('_secret')[0]
        
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Update metadata for products
        if product_pid:
            stripe.PaymentIntent.modify(product_pid, metadata={
                'product_bag': json.dumps(request.session.get('product_bag', {})),
                'save_info': request.POST.get('save_info'),
                'bag_type': 'product',
                'username': request.user,
            })

        # Update metadata for subscriptions
        if subscription_pid:
            stripe.PaymentIntent.modify(subscription_pid, metadata={
                'plan_bag': json.dumps(request.session.get('plan_bag', {})),
                'save_info': request.POST.get('save_info'),
                'bag_type': 'subscription',
                'username': request.user,
            })

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    product_bag = request.session.get('product_bag', {})
    plan_bag = request.session.get('plan_bag', {})

    if request.method == 'POST':
        is_product_order = bool(product_bag) and 'product_client_secret' in request.POST
        is_subscription_order = bool(plan_bag) and 'subscription_client_secret' in request.POST
								
        if not product_bag and not plan_bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('home'))
        
        if is_product_order:
            form_data = {
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                'town_or_city': request.POST['town_or_city'],
                'street_address1': request.POST['street_address1'],
                'street_address2': request.POST['street_address2'],
                'county': request.POST['county'],
            }
            order_form = OrderForm(form_data)

            if order_form.is_valid():
                order = order_form.save(commit=False)
                pid = request.POST.get('product_client_secret').split('_secret')[0]
                order.stripe_pid = pid
                order.original_bag = json.dumps(product_bag)
                order.save()

                # Creating Orderlineitem for each product
                for item_id, item_data in product_bag.items():
                    try:
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                        else:
                            for size, quantity in item_data['items_by_size'].items():
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                        order_line_item.save()
                    except Product.DoesNotExist:
                        messages.error(request, (
                            "One of the products in your bag wasn't found in our database. "
                            "Please call us for assistance!")
                        )
                        order.delete()
                        return redirect(reverse('view_bag'))

                # Save user information (if necessary)
                request.session['save_info'] = 'save-info' in request.POST

                # Redirecting to the page of successful ordering
                return redirect(reverse('order_success', args=[order.order_number]))

            else:
                messages.error(request, 'There was an error with your form. Please double check your information.')

        # Subscription processing
        elif is_subscription_order:
            form_data = {
                'full_name': request.POST.get('full_name', ''),
                'email': request.POST.get('email', ''),
            }
            subscription_form = SubscriptionForm(form_data)

            if subscription_form.is_valid():
                pid = request.POST.get('subscription_client_secret', '').split('_secret')[0]
                original_bag = json.dumps(plan_bag)
                print(plan_bag)

                user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

                try:
                    # Create a subscription object
                    subscription = subscription_form.save(commit=False)
                    subscription.stripe_pid = pid
                    subscription.original_bag = original_bag
                    subscription.user_profile = user_profile
                    subscription.save()

                    for item_id, item_data in plan_bag.items():
                        try:
                            plan = clone_plan(SubscriptionPlan.objects.get(id=item_id))

                            quantity = item_data.get('quantity', 1)

                            # Create a line item for the plan
                            line_item = SubscriptionLineItem(
                                subscription=subscription,
                                plan=plan,
                                quantity=quantity,
                            )
                            line_item.save()

                        except SubscriptionPlan.DoesNotExist:
                            messages.error(request, (
                                f"Plan with ID {item_id} wasn't found in our database. "
                                "Please call us for assistance!")
                            )
                            subscription.delete()  # Rollback subscription if any plan is missing
                            return redirect(reverse('view_bag'))

                    # Get the subscription number
                    subscription_number = subscription.subscription_number

                    # Update the total subscription amount after adding all lineitems
                    subscription.subscription_total = subscription.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
                    subscription.save()

                    # Save user information (if necessary)
                    request.session['save_info'] = 'save-info' in request.POST

                    # Redirect to the successful subscription page
                    return redirect(reverse('subscription_success', args=[subscription_number]))

                except Exception as e:
                    messages.error(request, f"An error occurred while processing your order: {str(e)}")
                    return redirect(reverse('view_bag'))

            else:
                messages.error(request, 'There was an error with your form. Please double check your information.')


    # If the request is not post, prepare forms for the render
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.full_name,
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })

            subscription_form = SubscriptionForm(initial={
                'full_name': profile.full_name,
                'email': profile.user.email,
            })

        except UserProfile.DoesNotExist:
            order_form = OrderForm()
            subscription_form = SubscriptionForm()
    else:
        order_form = OrderForm()
        subscription_form = SubscriptionForm()

    # Checking Stripe key
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    current_bag = bag_contents(request)
    stripe.api_key = stripe_secret_key

    if product_bag:
        # Calculate the amount for products
        product_total = current_bag['grand_product_total']
        stripe_product_total = round(product_total * 100)

        # Create a payment intention for products
        product_intent = stripe.PaymentIntent.create(
            amount=stripe_product_total,
            currency=settings.STRIPE_CURRENCY,
        )

    if plan_bag:
        # Calculate the amount for subscriptions
        subscription_total = current_bag['grand_plan_total']
        stripe_subscription_total = round(subscription_total * 100)

        # Create a payment intention for subscriptions
        subscription_intent = stripe.PaymentIntent.create(
            amount=stripe_subscription_total,
            currency=settings.STRIPE_CURRENCY,
        )

    context = {
        'order_form': order_form,
        'subscription_form': subscription_form,
        'stripe_public_key': stripe_public_key,
        'product_client_secret': product_intent.client_secret if product_bag else '',
        'subscription_client_secret': subscription_intent.client_secret if plan_bag else '',
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number=None, subscription_number=None):
    
    context = {}

    if order_number:
        save_info = request.session.get('save_info')
        # Processing a successful order of products
        order = get_object_or_404(Order, order_number=order_number)
        context['order'] = order

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            order.user_profile = profile
            order.save()

            if save_info:
                profile_data = {
                    'full_name': order.full_name,
                    'email': order.email,
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()

        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        # Cleaning the basket of products
        if 'product_bag' in request.session:
            del request.session['product_bag']

    elif subscription_number:
        save_info = request.session.get('save_info')
        # Successful subscription processing
        subscription = get_object_or_404(Subscription, subscription_number=subscription_number)
        context['subscription'] = subscription

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            subscription.user_profile = profile
            subscription.save()

            if save_info:
                # Update only full_name and email
                profile.full_name = subscription.full_name
                profile.email = subscription.email
                profile.save()

        messages.success(request, f'Order successfully processed! \
            Your order number is {subscription_number}. A confirmation \
            email will be sent to {subscription.email}.')

        # Cleaning the basket of subscriptions
        if 'plan_bag' in request.session:
            del request.session['plan_bag']

    else:
        messages.error(request, 'Invalid success request.')
        return redirect(reverse('home'))

    return render(request, 'checkout/checkout_success.html', context)