from django.urls import path
from . import views

urlpatterns = [
    path("watchlist", views.user_watchlist, name="watchlist"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("sign-up", views.user_signup, name="signup"),
]
