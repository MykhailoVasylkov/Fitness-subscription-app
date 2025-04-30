from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan

# Used code from Boutique Ado and Chat-GPT

def all_plans(request):
    """ A view to show all plans """

    plans = SubscriptionPlan.objects.all()
    nutrition_plans = SubscriptionPlan.objects.filter(category='nutrition')
    exercises_plans = SubscriptionPlan.objects.filter(category='exercises')

    context = {
        'plans': plans,
        'nutrition_plans': nutrition_plans,
        'exercises_plans': exercises_plans,
    }

    return render(request, 'plans/plans.html', context)


def plan_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    context = {
        'plan': plan,
    }

    return render(request, 'plans/plan_detail.html', context)
