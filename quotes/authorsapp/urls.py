from django.urls import path
from . import views

app_name = 'authorsapp'

urlpatterns = [
    path('author/', views.author, name='author'),
    path('author_detail/<int:author_id>', views.detail, name='author_detail'),
]

##     <!-- {% load extract_tags %} -->
##    <!-- {{ note.tags|tags }} -->