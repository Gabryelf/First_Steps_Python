from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:article_id>/delete/', views.article_delete, name='article_delete'),
]