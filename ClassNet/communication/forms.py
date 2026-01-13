# forms.py
from django import forms
from .models import StatusUpdate

class StatusUpdateForm(forms.ModelForm):
    """
    Form to handle the creation and update of status updates.

    This form is used to create or update a status update's content.
    It is based on the `StatusUpdate` model and only includes the `content` field,
    which represents the text of the status update.

    The form uses a `Textarea` widget for the `content` field with custom attributes:
    - A placeholder text ("What’s on your mind?").
    - A default number of rows (3) to display in the text area.

    Fields:
        content (CharField): The content of the status update.

    Meta:
        model (StatusUpdate): Specifies that this form is based on the `StatusUpdate` model.
        fields (list): Specifies that only the `content` field should be included in the form.
        widgets (dict): Customizes the form widget for the `content` field, using a `Textarea`
                        widget with custom attributes (placeholder and rows).
    """

    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'What’s on your mind?', 'rows': 3}),
        }
