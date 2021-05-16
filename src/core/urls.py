from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegistrationView, SetView, TestView, ResultView

app_name = 'core'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('sign_up/', RegistrationView.as_view(), name='sign_up'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),

    path('', SetView.as_view(), name='sets'),
    path('test/<str:slug>/<int:sequence>/', TestView.as_view(), name='test'),
    path('result/<str:slug>/', ResultView.as_view(), name='result'),
]
