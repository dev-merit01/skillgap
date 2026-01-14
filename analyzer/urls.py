"""
URL configuration for analyzer app.
"""
from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('app/', views.app, name='app'),
    path('home/', views.app, name='home'),
    path('analyze/', views.analyze, name='analyze'),
    path('extract-jd/', views.extract_jd_text, name='extract_jd'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
