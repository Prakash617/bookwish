from django import forms
from .models import PostEventFeedback

class FeedbackForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    is_interested = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = PostEventFeedback
        fields = '__all__'
