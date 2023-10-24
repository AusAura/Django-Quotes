from django.forms import ModelForm, CharField, TextInput
from .models import Quote, Tag


class QuoteForm(ModelForm):
    quote = CharField(min_length=20, max_length=150, required=True, widget=TextInput())
    
    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'authors']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']