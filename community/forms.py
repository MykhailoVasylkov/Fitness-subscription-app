from django import forms
from .models import CommunityPost
from .widgets import CustomClearableFileInput


class CommunityPostForm(forms.ModelForm):
    """
    A form for creating a post.
    """
    class Meta:
        model = CommunityPost
        fields = ['image', 'body']

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )
