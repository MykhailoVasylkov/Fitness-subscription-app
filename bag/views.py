from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    get_object_or_404,
)
from django.contrib import messages

from products.models import Product
from plans.models import SubscriptionPlan


# I used code snippet form Boutique Ado

def view_bag(request):
    """ A view that renders the bag contents page """
    template = 'bag/bag.html'
    context = {
        'on_bag_page': True
    }

    return render(request, template, context)


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    product_bag = request.session.get('product_bag', {})

    if size:
        if item_id in list(product_bag.keys()):
            if size in product_bag[item_id]['items_by_size'].keys():
                product_bag[item_id]['items_by_size'][size] += quantity
                messages.success(
                    request,
                    f'Updated size {size.upper()} {product.name} quantity to '
                    f'{product_bag[item_id]["items_by_size"][size]}'
                )
            else:
                product_bag[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request,
                    f'Added size {size.upper()} {product.name} to your bag'
                )
        else:
            product_bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request,
                f'Added size {size.upper()} {product.name} to your bag'
            )
    else:
        if item_id in list(product_bag.keys()):
            product_bag[item_id] += quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {product_bag[item_id]}'
            )
        else:
            product_bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['product_bag'] = product_bag
    return redirect(redirect_url)


def add_plan_to_bag(request, plan_id):
    """ Add a specified plan to the shopping bag """

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    redirect_url = request.POST.get('redirect_url')
    plan_bag = request.session.get('plan_bag', {})

    if plan:
        if plan_id in plan_bag:
            messages.info(request, f'Plan {plan.name} already in the bag')
        else:
            plan_bag[plan_id] = {'quantity': 1}
            messages.success(request, f'Added plan {plan.name} to your bag')

    request.session['plan_bag'] = plan_bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    product_bag = request.session.get('product_bag', {})

    if size:
        if quantity > 0:
            product_bag[item_id]['items_by_size'][size] = quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {product.name} quantity to'
                f'{product_bag[item_id]["items_by_size"][size]}'
            )
        else:
            del product_bag[item_id]['items_by_size'][size]
            if not product_bag[item_id]['items_by_size']:
                product_bag.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your bag'
            )
    else:
        if quantity > 0:
            product_bag[item_id] = quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {product_bag[item_id]}'
            )
        else:
            product_bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['product_bag'] = product_bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        product_bag = request.session.get('product_bag', {})

        if size:
            del product_bag[item_id]['items_by_size'][size]
            if not product_bag[item_id]['items_by_size']:
                product_bag.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your bag'
            )
        else:
            product_bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['product_bag'] = product_bag
        return HttpResponse(status=200)

    except Exception as e:

        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


def remove_plan_from_bag(request, plan_id):
    """ Remove the item from the shopping bag """

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    try:
        plan_bag = request.session.get('plan_bag', {})

        plan_bag.pop(plan_id)
        messages.success(request, f'Removed {plan.name} from your bag')

        request.session['plan_bag'] = plan_bag
        return HttpResponse(status=200)

    except Exception as e:

        messages.error(request, f'Error removing plan: {e}')
        return HttpResponse(status=500)
