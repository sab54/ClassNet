# forms.py
from django import forms
from .models import CourseFeedback

class CourseFeedbackForm(forms.ModelForm):
    """
    Form for submitting feedback for a course. 
    It allows users (typically students) to provide a rating and detailed feedback for a course they took.
    """
    class Meta:
        model = CourseFeedback
        fields = ['rating', 'feedback']
    
    # Make the rating a dropdown with the choices defined in the model
    rating = forms.ChoiceField(choices=CourseFeedback.RATING_CHOICES, widget=forms.Select())
    
    # Customize the widget for the feedback field
    widgets = {
        'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
    }

