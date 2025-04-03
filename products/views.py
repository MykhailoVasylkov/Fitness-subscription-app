from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models.functions import Lower

from .models import Product, Category

# Create your views here.
# Used code from Boutique Ado and Chat-GPT

def all_products(request):
    """ A view to show all products, including sorting queries """

    products = Product.objects.all()
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            
            # Determine what is transmitted in the GET request: ID (numbers) or names (rows)
            if categories[0].isdigit():
                products = products.filter(category__id__in=categories)
                categories = Category.objects.filter(id__in=categories)
            else:
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)
        else:
            categories = Category.objects.all()

        
    categories = Category.objects.filter(id__in=categories) if categories else Category.objects.all()

    current_sorting = f'{sort or "None"}_{direction or "None"}'

    all_categories = Category.objects.all()

    # Determine the current selected categories
    selected_categories = request.GET.get('category', '').split(',')

    context = {
        'products': products,
        'current_categories': categories,
        'all_categories': all_categories,
        'selected_categories': selected_categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
