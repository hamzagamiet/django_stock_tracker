from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stock/<str:pk>/", views.stock, name="stock"),
    path(
        "stock/<str:pk>/historical-data",
        views.stock_historical,
        name="stock_historical",
    ),
    path("stock/<str:pk>/data_api", views.get_data, name="api_data"),
    path("results/", views.search_results, name="results"),
    path("add_watch", views.add_watchlist, name="add_watchlist"),
]
