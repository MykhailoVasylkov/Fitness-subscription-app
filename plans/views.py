from django.shortcuts import render
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
