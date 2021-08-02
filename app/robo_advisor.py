# this is the "app/robo_advisor.py" file

import datetime
import requests
import csv
import json
from pandas import DataFrame

import os
from dotenv import load_dotenv

load_dotenv()

import re
import sys 

# 
# Inputs
# 

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

api_key = os.getenv("ALPHAVANTAGE_API_KEY") 

symbol = input("Please input a stock symbol: ")
symbol = symbol.upper()
if not re.match("^[A-Z]*$", symbol):
    sys.exit("Error! Expecting a properly-formed stock symbol like 'MSFT'. Run the app and try again")
elif len(symbol) > 5:
    sys.exit("Opps! Too many characters. Run the app and try again")


# request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
# print(type(response)) # <class 'requests.models.Response'>
# print(response.status_code) # 200
# print(response.text) # Dictionary

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

# breakpoint()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # sort to ensure latest day is first

latest_day = dates[0]

latest_closing_price = tsd[latest_day]["4. close"]

# maximum of all high prices

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))


recent_high = max(high_prices)
recent_low = min(low_prices)


# breakpoint()

datetime.datetime.now()

# 
# Info Outputs 
# 

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", datetime.datetime.now()) # https://docs.python.org/3/library/datetime.html
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_closing_price))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: Because the robot says so!")
print("-------------------------")
print("WRITING DATA TO CSV...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

for date in dates:
    daily_prices = tsd[date]

# Pandas
# print(tsd)
# breakpoint()
# d = {'1. open','2. high', '3. low', '4. close'}
df = DataFrame(tsd)
dft = df.transpose()
print(dft)
dft.rename(columns = {' ':'Timestamp', '1. open':'Open', '2. high':'High', '3. low':'Low','4. close':'Close', '6. volume':'Volume'}, inplace=True)
dft = dft.rename_axis("Timestamp")
print(dft)


dft.to_csv(f'/Users/devincremeans/Documents/GitHub/robo-advisor/data_{datetime.datetime.now()}.csv')
