import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import datetime as dt


account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_params = {
    "q": COMPANY_NAME,
    "apikey": "KEY",
    "sortBy": "popularity",
}

stock_params = {
    "apikey": "KEY",
    "symbol": STOCK,
    "function": "TIME_SERIES_INTRADAY",
    "outputsize": "full"   
}

OPEN_TIME = "04:00:00"
CLOSING_TIME = "19:55:00"

def get_stock_opening_closing(stock):
    stock_response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&outputsize=full&apikey={KEY}")
    stock_data = stock_response.json()
    stock_values = []
    for timestamp, values in stock_data["Time Series (5min)"].items():
        if "04:00:00" in timestamp or "19:55:00" in timestamp:
            open_values = values["1. open"]
            close_values = values["4. close"]
            stock_values.append({
                "date": timestamp,
                "price": {
                    "open": open_values,
                    "close": close_values
                }
            })
    return stock_values

stock_prices = get_stock_opening_closing(STOCK)[:3]

current_date = dt.datetime.now()
# for testing
current_date = "2023-08-11"

current_open = float(stock_prices[0]["price"]["open"])

def check_difference(open_price, stock):
    for day in stock[1:]:
        diff = open_price - float(day["price"]["close"])/open_price * 100
        if diff >= 5 or diff <= -5:
            return [True, diff]
        
    return [False, diff]

big_change = check_difference(current_open, stock_prices)

if big_change[0]:
    news_response = requests.get(NEWS_ENDPOINT, params = news_params)
    news_data = news_response.json()
    
    news_info = []
    for data in news_data["articles"][0:3]:
        news_info.append({
            "source": data["source"]["name"],
            "info":{
                "title": data["title"],
                "description": data["description"]
            }
        })

    if big_change[1] > 0:
        arrow = "🔺"
    else:
        arrow = "🔻"
    for x in news_info:
        print(f"{STOCK}{arrow}{big_change[1]:.2f%}\nHeadline:{x['info']['title']}\nBrief: {x['info']['description']}")
        
    # #print(f"{STOCK}{arrow}{big_change[1]}\nHeadline:{news_info[0]['title']}\nBrief: {news_info[0]['description']}")
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    # client = Client(account_sid, auth_token, http_client=proxy_client)
    #
    # for text in news_info:
    #     message = client.messages \
    #         .create(
    #         body=f"{STOCK}{arrow}{big_change[1]:.2f%}\nHeadline:{x['info']['title']}\nBrief: {x['info']['description']}",
    #         from_="YOUR TWILIO VIRTUAL NUMBER",
    #         to="YOUR TWILIO VERIFIED REAL NUMBER"
    #     )
    # print(message.status)
    
