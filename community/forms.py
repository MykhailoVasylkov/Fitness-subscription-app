from django import forms
from .models import CommunityPost


class CommunityPostForm(forms.ModelForm):
    """
    A form for creating a post.
    """
    class Meta:
        model = CommunityPost
        fields = ['image', 'body']