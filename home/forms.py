from django import forms
from .models import NewsletterSubscriber


class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Type your email here',
            'class': 'form-control',
        })
