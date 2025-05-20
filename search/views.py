from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, SubscriptionPlan

def search(request):
    query = request.GET.get('q')
    if not query:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))

    search_filter = Q(name__icontains=query) | Q(description__icontains=query)

    products = Product.objects.filter(search_filter)
    plans = SubscriptionPlan.objects.filter(search_filter)

    return render(request, 'search_results.html', {
        'search_term': query,
        'products': products,
        'plans': plans,
    })
