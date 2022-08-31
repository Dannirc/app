from django.contrib.auth.views import LogoutView
from django.urls import path

from core.login.views import LoginFormView, LoggedFormView

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logged/', LoggedFormView.as_view(), name='logged'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
