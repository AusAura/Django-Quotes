from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('find_tag/<str:tag_name>', views.find_tag, name='find_tag'),
    path('scrap/<str:url>', views.scrap_view, name='scrap'),
]

##             <a href="{% url 'quotesapp:delete' quote.id %}" role="button" class="contrast"> Delete note </a>