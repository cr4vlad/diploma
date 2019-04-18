from django import forms
from .models import Post

class NewRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('title', 'description')