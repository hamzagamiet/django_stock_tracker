from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.contrib import messages
from projects.models import Watchlist
from django.contrib.auth.models import User
from .models import Profile
from projects.views import get_stock_data as get_data
from .forms import CustomUserCreationForm


# Create your views here.
@login_required(login_url="login")
def user_watchlist(request):
    """
    *Require user login
    Query database to get list of user's watchlisted stocks
    Output list of user's stocks along with stock information
    """
    username = request.user.username
    print("watchlist for", username)
    watch = Watchlist.objects.filter(watcher=username)
    ticker_list = [stock.ticker for stock in watch if username == stock.watcher]
    stock_list = [get_data(ticker)["stock_obj"] for ticker in ticker_list]
    i = 0
    for stock in stock_list:
        i += 1
        stock["rank"] = i

    context = {
        "username": username,
        "ticker_list": ticker_list,
        "stock_list": stock_list,
    }

    return HttpResponse(render(request, "users/watchlist.html", context))


def user_login(request):
    """
    Take user input, query with data base for matches and allow/reject user login
    """
    if request.user.is_authenticated:
        return redirect("home")
    print("attempting log in")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("done")
            return redirect("home")
        else:
            messages.error(request, "Username OR Password incorrect")
    return HttpResponse(render(request, "users/login.html"))


def user_logout(request):
    """
    Sign user out of session
    """
    logout(request)
    messages.error(request, "User was logged out")
    return redirect("login")


def user_signup(request):
    """
    Take user input, query with data base for matches and allow/reject user registration
    If no matches in database, allow user signup
    """
    if request.user.is_authenticated:
        return redirect("home")
    context = {}
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Account successfully created")

            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error has ocurred during registration")
    return HttpResponse(render(request, "users/signup.html", {"form": form}))
