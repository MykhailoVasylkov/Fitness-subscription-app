from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib import messages
from settings.models import DeliverySettings
from products.models import Product
from plans.models import SubscriptionPlan

# I used code snippet form Boutique Ado 

def delivery_settings(request):
    settings = DeliverySettings.get_solo()
    return {
        'FREE_DELIVERY_THRESHOLD': settings.free_delivery_threshold,
        'STANDARD_DELIVERY_PERCENTAGE': settings.standard_delivery_percentage,
    }


def bag_contents(request):
    product_items = []
    plan_items = []

    total_product = 0
    total_plan = 0
    product_count = 0
    plan_count = 0

    product_bag = request.session.get('product_bag', {})
    plan_bag = request.session.get('plan_bag', {})

    if len(plan_bag) > 1:
        messages.error(request, "You can only purchase one subscription plan at a time.")

    delivery_settings_data = delivery_settings(request)

    for item_id, item_data in product_bag.items():

        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total_product += item_data * product.price
            product_count += item_data
            product_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
            
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total_product += quantity * product.price
                product_count += quantity
                product_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    for plan_id, plan_data in plan_bag.items():
        plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
        total_plan += plan_data['quantity'] * plan.price
        plan_count += plan_data['quantity']
        plan_items.append({
            'plan_id': plan_id,
            'quantity': plan_data['quantity'],
            'plan': plan,
            'duration_weeks': plan.duration_weeks,
            'level': plan.level,
        })
    
    total = total_product + total_plan

    if total_product < delivery_settings_data['FREE_DELIVERY_THRESHOLD']:
        delivery = total_product * Decimal(delivery_settings_data['STANDARD_DELIVERY_PERCENTAGE'] / 100)
        free_delivery_delta = delivery_settings_data['FREE_DELIVERY_THRESHOLD'] - total_product
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    grand_product_total = delivery + total_product
    
    context = {
        'product_items': product_items,
        'plan_items': plan_items,
        'total': total,
        'product_count': product_count,
        'plan_count': plan_count,
        'total_count': product_count + plan_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': delivery_settings_data['FREE_DELIVERY_THRESHOLD'],
        'grand_total': grand_total,
        'grand_product_total': grand_product_total,
        'total_plan': total_plan,
        'total_product': total_product,
        
    }

    return context