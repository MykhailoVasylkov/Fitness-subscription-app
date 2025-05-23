from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from products.models import Product
from plans.models import SubscriptionPlan


def search(request):
    query = request.GET.get('q')
    if not query:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('home'))

    search_filter = Q(name__icontains=query) | Q(description__icontains=query)

    products = Product.objects.filter(search_filter)
    nutrition_plans = (
        SubscriptionPlan.objects
        .filter(category='nutrition')
        .filter(search_filter)
    )
    exercises_plans = (
        SubscriptionPlan.objects
        .filter(category='exercises')
        .filter(search_filter)
    )

    return render(request, 'search/search_results.html', {
        'search_term': query,
        'products': products,
        'nutrition_plans': nutrition_plans,
        'exercises_plans': exercises_plans,
    })
