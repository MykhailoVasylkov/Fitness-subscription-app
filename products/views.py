from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from .models import Product, Category, ProductSize, Brand, ProductReview
from .forms  import ProductForm, ProductReviewForm


# Create your views here.
# Used code from Boutique Ado and Chat-GPT

def all_products(request):
    """ A view to show all products, including sorting queries """

    products = Product.objects.all()
    categories = None
    sort = None
    direction = None
    selected_brands = []
    min_price = None
    max_price = None

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
        
        # Filtering by brand
        if 'brand' in request.GET and request.GET['brand']:
            brands = request.GET['brand'].split(',')
            products = products.filter(brand__name__in=brands)
            selected_brands = brands
        else:
            selected_brands = []

        # Filtering by category   
        if 'category' in request.GET and request.GET['category']:
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
        
        # Filtering by price range
        if 'min_price' in request.GET and request.GET['min_price']:
            min_price = int(request.GET['min_price'])
            products = products.filter(price__gte=min_price)
        
        if 'max_price' in request.GET and request.GET['max_price']:
            max_price = int(request.GET['max_price'])
            products = products.filter(price__lte=max_price)

    current_sorting = f'{sort or "None"}_{direction or "None"}'

    all_categories = Category.objects.all()

    # Determine the current selected categories
    selected_categories = request.GET.getlist('category')

    all_brands = Brand.objects.all()

    context = {
        'products': products,
        'all_categories': all_categories,
        'selected_categories': selected_categories,
        'current_sorting': current_sorting,
        'all_brands': all_brands,
        'selected_brands': selected_brands,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details, review form and existing reviews """

    product = get_object_or_404(Product, pk=product_id)

    reviews = product.product_reviews.filter(approved=True).order_by("-created_on")

    user_reviews = None
    if request.user.is_authenticated:
        user_reviews = product.product_reviews.filter(author=request.user)

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to submit a review.')
            return redirect('account_login') 
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.product = product
            review.save()

            messages.success(request, 'Review submitted and awaiting approval')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to submit review!')
    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'form': form,
        'reviews': reviews,
        'user_reviews': user_reviews,
        'user_profile': user_profile,
    }

    return render(request, 'products/product_detail.html', context)


def edit_product_review(request, product_id, pk):
    """
    Edit an existing instance of model:`products.ProductReview`.

    """
    review = get_object_or_404(ProductReview, pk=pk)
    product = review.product

    if request.method == 'POST':

        form = ProductReviewForm(data=request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your review has been updated.'
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Error updating review!'
            )
    else:
        form = ProductReview(instance=review)

    return redirect('product_detail', product_id=product.id)


def delete_product_review(request, product_id, pk):
    """
    Delete an existing instance of model:`products.ProductReview`.

    """
    review = get_object_or_404(ProductReview, pk=pk)
    product = review.product
    if request.method == "POST":
        if review.author == request.user:
            review.delete()
            messages.add_message(
                request, messages.SUCCESS,
                'Your review has been deleted.'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'Error deleting review!'
            )

    return redirect('product_detail', product_id=product.id)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('home')

    SizesFormset = inlineformset_factory(Product, ProductSize, fields=['size', 'quantity'], extra=0)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = SizesFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            messages.success(request, 'Successfully added product!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        formset = SizesFormset()

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'products/add_product.html', context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    SizesFormset = inlineformset_factory(
    Product, ProductSize,
    fields=['size', 'quantity'],
    extra=0,
    can_delete=True
    )

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = SizesFormset(request.POST, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        formset = SizesFormset(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'formset': formset,
        
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))