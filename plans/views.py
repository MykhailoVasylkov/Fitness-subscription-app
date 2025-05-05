from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan

# Used code from Boutique Ado and Chat-GPT

def all_plans(request):
    """ A view to show all plans """

    nutrition_plans = SubscriptionPlan.objects.filter(category='nutrition')
    exercises_plans = SubscriptionPlan.objects.filter(category='exercises')
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            nutrition_plans = nutrition_plans.order_by(sortkey)
            exercises_plans = exercises_plans.order_by(sortkey)
    
    current_sorting = f'{sort or "None"}_{direction or "None"}'

    context = {
        'nutrition_plans': nutrition_plans,
        'exercises_plans': exercises_plans,
        'current_sorting': current_sorting,
    }

    return render(request, 'plans/plans.html', context)


def plan_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    context = {
        'plan': plan,
    }

    return render(request, 'plans/plan_detail.html', context)
