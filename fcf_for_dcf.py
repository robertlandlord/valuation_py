import pandas as pd


def get_fcf_growth(stock):
    url = 'https://www.marketwatch.com/investing/stock/' + stock + '/financials/cash-flow'

    dfs = pd.read_html(url)
    df = dfs[2]
    year_1_fcf = 0.0
    year_2_fcf = 0.0
    year_3_fcf = 0.0
    year_4_fcf = 0.0
    year_5_fcf = 0.0

    for index, row in df.iterrows():
        if row[0] == 'Free Cash Flow':
            year_1_fcf = text_to_num(row[1])
            year_2_fcf = text_to_num(row[2])
            year_3_fcf = text_to_num(row[3])
            year_4_fcf = text_to_num(row[4])
            year_5_fcf = text_to_num(row[5])
    avg_fcf_growth = ((year_2_fcf-year_1_fcf)/year_1_fcf + (year_3_fcf-year_2_fcf)/year_2_fcf +
                      (year_4_fcf-year_3_fcf)/year_3_fcf + (year_5_fcf-year_4_fcf)/year_4_fcf)/4.0

    if avg_fcf_growth < 0:
        avg_fcf_growth = (year_5_fcf-year_1_fcf)/year_1_fcf/4

    # if a lot of irregularity, i.e. if all else fails
    if avg_fcf_growth > .2:
        avg_fcf_growth = .08

    return avg_fcf_growth


def get_starting_fcf(stock):
    url = 'https://www.marketwatch.com/investing/stock/' + stock + '/financials/cash-flow'

    dfs = pd.read_html(url)
    df = dfs[2]
    year_1_fcf = 0.0
    year_2_fcf = 0.0
    year_3_fcf = 0.0
    year_4_fcf = 0.0
    year_5_fcf = 0.0

    for index, row in df.iterrows():
        if row[0] == 'Free Cash Flow':
            year_1_fcf = text_to_num(row[1])
            year_2_fcf = text_to_num(row[2])
            year_3_fcf = text_to_num(row[3])
            year_4_fcf = text_to_num(row[4])
            year_5_fcf = text_to_num(row[5])
    avg_fcf = (year_1_fcf + year_2_fcf + year_3_fcf + year_4_fcf + year_5_fcf)/5
    return avg_fcf


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
            num = ''
            for index in range(1, len(text)-1):
                if text[index] != ',':
                    num = num + text[index]
            return float(num)*-1
    else:
        num = ''
        for index in range(0, len(text)):
            if text[index] != ',':
                num = num + text[index]
        return float(num)
