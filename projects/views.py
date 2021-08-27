from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from pandas.core.frame import DataFrame
from pandas_datareader import data as web
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import pandas as pd
import datetime
from datetime import date
import json
import requests
from django.contrib.auth.models import User
import os
from users.models import Profile
from .models import Watchlist
from pathlib import Path
from django.http import HttpResponseRedirect


def home(request):
    """
    Get several stock data from get_stock_data and output to home page
    """
    ticker_list = ["GOOG", "FB", "AMZN", "NFLX", "F"]
    stock_list = [get_stock_data(x)["stock_obj"] for x in ticker_list]
    i = 0
    for stock in stock_list:
        i += 1
        stock["rank"] = i
    return HttpResponse(
        render(request, "projects/home.html", {"stock_list": stock_list})
    )


def check_watchlist(username, stock):
    """
    Check to see how many watchlists stock exists on and if stock exists on current user's watchlist
    """
    add_to_watch = True
    tot_watchlists = 0
    for person in Watchlist.objects.filter(ticker=stock):
        tot_watchlists += 1
        if person.watcher == username:
            add_to_watch = False
    context = {"add_to_watch": add_to_watch, "tot_watchlists": tot_watchlists}
    return context


def stock(request, pk):
    """
    Get individiual stock data from get_stock_data and output to individual stock page
    """
    try:
        username = request.user.username
    except:
        username = None
    stock_obj = get_stock_data(pk)["stock_obj"]
    stock_info = get_stock_data(pk)["stock_info"]
    add_to_watch = check_watchlist(username, pk)["add_to_watch"]
    tot_watchlists = check_watchlist(username, pk)["tot_watchlists"]
    context = {
        "stock_obj": stock_obj,
        "add_to_watch": add_to_watch,
        "tot_watchlists": tot_watchlists,
    }
    return HttpResponse(render(request, "projects/stock.html", context))


def get_data(request, pk):
    """
    Get data from get_stock_data function and create Json response
    """
    data = get_stock_data(pk)
    return JsonResponse(data)


def stock_historical(request, pk):
    """
    Output put historical data from Yahoo API
    """
    try:
        username = request.user.username
    except:
        username = None
    stock_obj = get_stock_data(pk)["stock_obj"]
    stock_info = get_stock_data(pk)["stock_info"]
    add_to_watch = check_watchlist(username, pk)["add_to_watch"]
    tot_watchlists = check_watchlist(username, pk)["tot_watchlists"]
    context = {
        "stock_info": stock_info,
        "stock_obj": stock_obj,
        "add_to_watch": add_to_watch,
        "tot_watchlists": tot_watchlists,
    }

    return HttpResponse(render(request, "projects/historical-data.html", context))


def get_stock_data(symbol):
    """
    Retrieve stock data from Yahoo, Nasdaq and Alpha Vantage APIs
    """
    # GET NASDAQ INFO
    nasdaq_symbols = get_nasdaq_symbols()
    # STOCK NAMES TOO LONG - SHORTEN
    stock_name_long = nasdaq_symbols.loc[symbol]["Security Name"]
    stock_name_short = (
        (stock_name_long[:40] + "...") if len(stock_name_long) > 40 else stock_name_long
    )
    try:
        url = (
            "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
            + symbol
            + "&interval=5min&outputsize=full&apikey=DL2U6G9UFXX85ORZ"
        )
        r = requests.get(url)
        data_intraday = r.json()
        last_refresh = data_intraday["Meta Data"]["3. Last Refreshed"]
        price = data_intraday["Time Series (5min)"][last_refresh]["4. close"]
    except:
        price = "Call limit reached. Wait 1 minute."

    start = datetime.datetime(2015, 1, 1)
    end = date.today()
    stock_info = []
    try:
        stock = web.DataReader(symbol, "yahoo", start, end)
        nasdaq_symbols = pd.DataFrame(stock)
        nasdaq_symbols = nasdaq_symbols.reset_index(level=["Date"])
        nasdaq_symbols = nasdaq_symbols.sort_index(ascending=False)
        nasdaq_symbols.reset_index(drop=True, inplace=True)
        daily_change = (nasdaq_symbols["Close"][0]) / (nasdaq_symbols["Close"][1]) - 1
        weekly_change = (nasdaq_symbols["Close"][0]) / (nasdaq_symbols["Close"][6]) - 1
        vol_daily_change = (nasdaq_symbols["Volume"][0]) / (
            nasdaq_symbols["Volume"][1]
        ) - 1
        vol_weekly_change = (nasdaq_symbols["Volume"][0]) / (
            nasdaq_symbols["Volume"][6]
        ) - 1

        # STOCK OBJ
        stock_obj = {
            "ticker": symbol,
            "stock_name_short": stock_name_short,
            "stock_name_long": stock_name_long,
            "price": price,
            "high": round(nasdaq_symbols["High"][0], 2),
            "low": round(nasdaq_symbols["Low"][0], 2),
            "open": round(nasdaq_symbols["Open"][0], 2),
            "close": round(nasdaq_symbols["Close"][0], 2),
            "daily_change": round(daily_change, 4),
            "weekly_change": round(weekly_change, 4),
            "volume": int(nasdaq_symbols["Volume"][0]),
            "vol_daily_change": round(vol_daily_change, 4),
            "vol_weekly_change": round(vol_weekly_change, 4),
        }

        # STOCK INFO
        for x in range(nasdaq_symbols.shape[0]):
            stock_info.append(
                {
                    "date": nasdaq_symbols["Date"][x],
                    "high": round(nasdaq_symbols["High"][x], 2),
                    "low": round(nasdaq_symbols["Low"][x], 2),
                    "open": round(nasdaq_symbols["Open"][x], 2),
                    "close": round(nasdaq_symbols["Close"][x], 2),
                    "volume": int((nasdaq_symbols["Volume"][x])),
                }
            )

        return {"stock_obj": stock_obj, "stock_info": stock_info}
    except:

        # STOCK OBJ
        stock_obj = {
            "ticker": "N/A",
            "stock_name_short": "N/A",
            "stock_name_long": 0,
            "price": 0,
            "high": 0,
            "low": 0,
            "open": 0,
            "close": 0,
            "daily_change": 0,
            "weekly_change": 0,
            "volume": 0,
            "vol_daily_change": 0,
            "vol_weekly_change": 0,
        }

        # STOCK INFO
        stock_info = {
            "date": 2000 - 1 - 1,
            "high": 0,
            "low": 0,
            "open": 0,
            "close": 0,
            "volume": 0,
        }

        return {"stock_obj": stock_obj, "stock_info": stock_info}


def search_results(request):
    """
    Take search input and query with company/ticker names on Nasdaq API
    Output list of matches
    """
    if request.method == "POST":
        query = request.POST["search_query"]
        nasdaq_info = get_nasdaq_symbols()
        nasdaq_symbols = pd.DataFrame(nasdaq_info)
        # remove symbol from index & set to column
        nasdaq_symbols = nasdaq_symbols.reset_index(level=["Symbol"])
        nasdaq_symbols.reset_index(drop=True, inplace=True)
        match_list = []

        for x in range(nasdaq_symbols.shape[0]):
            # IF search result matches security name on Nasdaq stock exchange
            if query.lower() in nasdaq_symbols.loc[x]["Security Name"].lower():
                match_list.append(
                    {
                        "symbol": nasdaq_symbols.loc[x]["Symbol"],
                        "stock_name_long": nasdaq_symbols.loc[x]["Security Name"],
                        "stock_name_short": (
                            nasdaq_symbols.loc[x]["Security Name"][:40] + "..."
                        ),  # shortened version of key: "stock_name_long"
                    }
                )
            elif query.lower() in nasdaq_symbols.loc[x]["Symbol"].lower():
                # IF search result matches ticker name on Nasdaq stock exchange
                match_list.append(
                    {
                        "symbol": nasdaq_symbols.loc[x]["Symbol"],
                        "stock_name_long": nasdaq_symbols.loc[x]["Security Name"],
                        "stock_name_short": (stock_name_long[:40] + "...")
                        if len(stock_name_long) > 40
                        else stock_name_long,
                    }
                )

        context = {
            "query": query,
            "match_list": match_list,
            "match_number": len(match_list),
        }
        return HttpResponse(render(request, "projects/results.html", context))
    else:
        return HttpResponse(render(request, "projects/results.html"))


def add_watchlist(request):
    """
    Take user input and add stock to stocklist
    """
    if request.method == "POST":
        try:
            ticker = request.POST["add_watchlist"]
            if request.user.is_authenticated:
                username = request.user.username
                Watchlist.objects.create(watcher=username, ticker=ticker)
        except:
            return redirect("watchlist")
    return redirect("watchlist")
