from django.urls import path
from AudioText2SignLangApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('animation/', views.animation, name='animation'),
    path('profile/', views.profile_view, name='profile'),
]
