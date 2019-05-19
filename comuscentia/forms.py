from django import forms
from django.forms import Textarea
from .models import Room

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('title', 'description', 'textblock', 'close')
        widgets = {
            'title': Textarea(attrs={'cols': 50, 'rows': 1}),
            'description': Textarea(attrs={'cols': 50, 'rows': 5}),
            'textblock': Textarea(attrs={'cols': 50, 'rows': 10}),
        }