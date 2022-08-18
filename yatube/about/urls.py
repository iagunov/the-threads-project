from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(
        template_name='about/author.html'), name='author'),
    path('tech/', views.AboutTechView.as_view(
        template_name='about/tech.html'), name='tech'),
]
