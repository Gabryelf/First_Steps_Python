from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blocks/', views.blocks_demo, name='blocks'),
    path('variables/', views.variables_demo, name='variables'),
    path('filters/', views.filters_demo, name='filters'),
    path('tags/', views.tags_demo, name='tags'),
    path('inheritance/', views.inheritance_demo, name='inheritance'),
    path('includes/', views.includes_demo, name='includes'),
]
