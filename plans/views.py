from django.shortcuts import render
from .models import SubscriptionPlan

# Used code from Boutique Ado and Chat-GPT

def all_plans(request):
    """ A view to show all products, including sorting queries """

    plans = SubscriptionPlan.objects.all()

    context = {
        'plans': plans,
    }

    return render(request, 'plans/plans.html', context)
