import datetime as dt
from matplotlib import style
import pandas_datareader.data as web
import time
from dcf import dcf
from dd import dd


stock = input("What stock (insert as ticker symbol) are you trying to evaluate today?")
print('Okay, lets run a valuation for $'+stock.upper())

style.use('ggplot')
start = dt.datetime(2015,1,1)
end = dt.datetime.now()
try:
    df = web.DataReader(stock, 'morningstar', start, end, retry_count=0)
except ValueError:
    print("Invalid ticker symbol, please restart program again.")
    quit()
time.sleep(1)
print('Here\'s some data for $'+stock+' as of today...')
time.sleep(1)
print(df.tail())

print("What type of valuation would you like to conduct?")
valType = ""
valTypeCounter = 0

# prompts user for type of valuation
while valType != 'DD' and valType != "DCF":
    if valTypeCounter > 0:
        print("Please enter either 'DCF' or 'DD'")
    valType = input("For a Discounted Cash Flows, enter 'DCF'. For a Discounted Dividends, enter 'DD'.")
    valType = valType.upper()
    valTypeCounter += 1

print('Okay, lets run a '+valType+' valuation.')

cases = {
    "DCF": dcf,
    "DD": dd,
}

cases[valType](stock)






