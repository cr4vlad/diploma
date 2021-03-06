from django import forms
from django.forms import Textarea
from .models import Room

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('title', 'description', 'textblock')#, 'close')
        widgets = {
            'title': Textarea(attrs={'cols': 50, 'rows': 1}),
            'description': Textarea(attrs={'cols': 50, 'rows': 5}),
            'textblock': Textarea(attrs={'cols': 50, 'rows': 10}),
        }

class SearchForm(forms.Form):
	search_field = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'id':'search_field'}))

class MessageForm(forms.Form):
	message_field = forms.CharField(label="", max_length=10000, widget=forms.TextInput(attrs={'id':'message_field', 'placeholder': 'Message'}))

class MailingForm(forms.Form):
	subject_field = forms.CharField(label="", widget=forms.TextInput(attrs={'id':'subject_field', 'placeholder': 'Subject'}))
	mail_field = forms.CharField(label="", widget=Textarea(attrs={'id':'mail_field', 'placeholder': 'Message'}))