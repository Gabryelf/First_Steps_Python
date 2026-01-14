from django.urls import path
from . import views

urlpatterns = [                                                # <all 8
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.user_list_view, name='user_list'),
]