from django import forms
from .models import PlanReview


class PlanReviewForm(forms.ModelForm):
    """
    A form for creating a single review.
    """
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)

    class Meta:
        model = PlanReview
        fields = ['author', 'rating', 'body', ]
