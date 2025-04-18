from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

'''
Code snippet fro Boutique Ado
'''
class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Profile Image')
    input_text = _('')
    template_name = 'profiles/custom_widget_templates/custom_clearable_file_input.html'