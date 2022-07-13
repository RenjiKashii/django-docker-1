from django import forms

from . import models


class SnippetForm(forms.ModelForm):
    class Meta:
        model = models.Snippet
        fields = ('title', 'code', 'description')