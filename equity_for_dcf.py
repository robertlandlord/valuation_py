import pandas as pd
import pandas_datareader as web
import datetime as dt
from scipy import stats
import urllib.request
import bs4 as bs




def get_coe_capm(stock):
    # Risk Free Rate
    rfr = .0293
    print('Risk free rate currently set at US 10Y T-bond rate(', rfr * 100, '%).')
    rfr_change = (input("enter 'Y' to change, else press enter")).upper()
    if rfr_change == 'Y':
        rfr = input_float("Enter new rfr as a decimal")
        rfr_print = rfr * 100
        print('New Risk Free Rate is ', rfr_print, '%.')

    # Market Risk Premium
    mrp = .051
    print('Market Risk Premium currently using damodaran estimate(', mrp * 100, '%).')
    mrp_change = (input("enter 'Y' to change, else press enter")).upper()
    if mrp_change == "Y":
        mrp = input_float("Enter new mrp as a decimal")
        mrp_print = mrp * 100
        print('New Market Risk Premium is ', mrp_print, '%.')

    # Beta
    beta_val = beta(stock)
    cost_of_equity = rfr+beta_val*mrp
    return cost_of_equity


def beta(stock): #currently only able to get a daily beta from 2015, need to find way to resample data for monthly data
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime.now()

    stock_df = web.DataReader(stock, 'morningstar', start, end)
    # print(stock_df.head())
    # stock_df.Date = pd.to_datetime(stock_df.Date)
    # stock_df = stock_df.resample('M').sum()
    # print(stock_df.head())
    stock_df.reset_index(drop=True, inplace=True)

    sp500_df = web.DataReader('spy', 'morningstar', start, end)

    # print(sp500_df.head())
    sp500_df.reset_index(drop=True, inplace=True)

    monthly_prices = pd.concat([stock_df['Close'], sp500_df['Close']], axis=1)
    monthly_prices.columns = [stock.upper(), 'SPY']

    # print(monthly_prices.head())

    # calculating monthly returns
    monthly_returns = monthly_prices.pct_change(1)
    clean_monthly_returns = monthly_returns.dropna(axis=0)
    # print(clean_monthly_returns)

    x = clean_monthly_returns['SPY']
    y = clean_monthly_returns[stock.upper()]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print('Your daily beta for $'+stock.upper()+' is ', round(slope, 2))

    return slope


def get_mv_equity(stock):
    url = "https://finance.yahoo.com/quote/" + stock + "?p=" + stock
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    data_list = list()
    market_cap = 0.0
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            for data in row.find_all('td'):
                data_list.append(data.text)

    for index in range(0,len(data_list)):
        if data_list[index] == 'Market Cap':
            market_cap = data_list[index+1]

    return text_to_num(market_cap)/1000000.0


def get_shares_outstanding(stock):
    url = 'https://finance.yahoo.com/quote/' + stock + '/key-statistics/'
    dfs = pd.read_html(url)
    df = dfs[8]
    data = df.ix[2]
    return text_to_num(data[1])


def text_to_num(text):
    d = {
        'T': 3,
        'M': 6,
        'B': 9
    }
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return float(num) * 10 ** d[magnitude]
    elif text[-1] == ')':
        if text[-2] in d:
            num = text[1:-2]
            magnitude = text[-2]
            return float(num) * -1 * 10**d[magnitude]
    else:
        return float(text)


def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('invalid number, try again')
