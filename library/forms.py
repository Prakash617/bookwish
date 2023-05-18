from django import forms
from .models import *

class GoogleBooksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = GoogleBooks
        fields = "__all__"
