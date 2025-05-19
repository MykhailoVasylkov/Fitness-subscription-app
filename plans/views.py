from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan


# Used code from Boutique Ado and Chat-GPT

def all_plans(request):
    """ A view to show all plans """

    nutrition_plans = SubscriptionPlan.objects.filter(category='nutrition')
    exercises_plans = SubscriptionPlan.objects.filter(category='exercises')
    sort = None
    direction = None
    selected_levels = []
    selected_durations = []
    min_price = None
    max_price = None

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

        # Filtering by duration
        if 'duration_weeks' in request.GET and request.GET['duration_weeks']:
            duration = int(request.GET['duration_weeks'])
            nutrition_plans = nutrition_plans.filter(duration_weeks=duration)
            exercises_plans = exercises_plans.filter(duration_weeks=duration)
            selected_durations = [duration]
        else:
            selected_durations = []

        # Filtering by level
        if 'level' in request.GET and request.GET['level']:
            level = int(request.GET['level'])
            nutrition_plans = nutrition_plans.filter(level=level)
            exercises_plans = exercises_plans.filter(level=level)
            selected_levels = [level]
        else:
            selected_levels = []

    # Filtering by price range
        if 'min_price' in request.GET and request.GET['min_price']:
            min_price = int(request.GET['min_price'])
            nutrition_plans = nutrition_plans.filter(price__gte=min_price)
            exercises_plans = exercises_plans.filter(price__gte=min_price)
        
        if 'max_price' in request.GET and request.GET['max_price']:
            max_price = int(request.GET['max_price'])
            nutrition_plans = nutrition_plans.filter(price__lte=max_price)
            exercises_plans = exercises_plans.filter(price__lte=max_price)
    
    current_sorting = f'{sort or "None"}_{direction or "None"}'

    all_durations = SubscriptionPlan.objects.values_list('duration_weeks', flat=True).distinct()

    all_levels = SubscriptionPlan._meta.get_field('level').choices

    context = {
        'nutrition_plans': nutrition_plans,
        'exercises_plans': exercises_plans,
        'current_sorting': current_sorting,
        'min_price': min_price,
        'max_price': max_price,
        'selected_levels': selected_levels,
        'selected_durations': selected_durations,
        'all_durations': all_durations,
        'all_levels': all_levels,
    }

    return render(request, 'plans/plans.html', context)


def plan_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    context = {
        'plan': plan,
    }

    return render(request, 'plans/plan_detail.html', context)


def review_create(request):
    """
    A view to render PlanReviewForm and existing reviews to the plans/plan_detail.html
    """
    reviews = PlanReview.objects.filter(approved=True).order_by("-created_on")

    user_reviews = None
    if request.user.is_authenticated:
        user_reviews = PlanReview.objects.filter(author=request.user)

    if request.method == 'POST':
        form = PlanReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            messages.success(request, 'Review submitted and awaiting approval')
            return redirect('contact')
        else:
            messages.error(request, f'Failed to submit review!')
    else:
        form = PlanReviewForm()

    return render(request, 'plans/plan_detail.html', {
        'form': form,
        'reviews': reviews,
        'user_reviews': user_reviews,
    })
