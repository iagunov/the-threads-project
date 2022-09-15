from django import forms
from .models import Idea, Opinion


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'tags', 'who_needed', 'text',)


class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ('text',)
