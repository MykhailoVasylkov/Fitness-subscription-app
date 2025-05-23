from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from .widgets import CustomClearableFileInput
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

    avatar = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        Separate fields into two formsets
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                "",
                "nickname",
                "full_name",
                "email",
            ),
            Fieldset(
                "Default Delivery Information",
                "default_phone_number",
                "default_street_address1",
                "default_street_address2",
                "default_town_or_city",
                "default_county",
                "default_postcode",
                "default_country",
            ),
        )

        placeholders = {
            "avatar": "Avatar",
            "nickname": "Nickname",
            "full_name": "Full Name",
            "email": "Email",
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        self.fields["nickname"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-3 profile-form-input"
            self.fields[field].label = False
