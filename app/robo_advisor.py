# this is the "app/robo_advisor.py" file

import requests

import json

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

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
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


# 
# Info Outputs 
# 

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_closing_price))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")