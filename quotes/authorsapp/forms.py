from django.forms import ModelForm, CharField, TextInput
from .models import Author


class AuthorForm(ModelForm):

    fullname = CharField(min_length=7, max_length=25, required=True, widget=TextInput())
    born_date = CharField(min_length=15, max_length=25, required=True, widget=TextInput())
    born_location = CharField(min_length=20, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=50, max_length=500, required=True, widget=TextInput())
    goodreads_url = CharField(min_length=15, max_length=80, required=False, widget=TextInput())
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description', 'goodreads_url']