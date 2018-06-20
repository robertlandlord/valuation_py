from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time


def get_debt_yield(stock):
    driver = webdriver.Chrome()
    driver.get("http://finra-markets.morningstar.com/MarketData/CompanyInfo/default.jsp")
    driver.implicitly_wait(1)
    # search the company
    text_box = driver.find_element_by_id("ms-finra-autocomplete-box")
    text_box.send_keys(stock)
    time.sleep(1)
    driver.find_element_by_css_selector(".button_blue.autocomplete-go").click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ms-equity-detail"]/div/div/div[1]/div[1]/div/div[1]/div[2]/ul/li[4]').click()
    driver.implicitly_wait(1)
    driver.find_element_by_class_name("ms-finra-more-bond").click()
    driver.implicitly_wait(1.5)
    driver.find_element_by_css_selector(".button_blue.agree").click()

    # average counter
    sum_yields = 0.0
    counter = 1
    valid_bond_counter = 0
    index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
        str(counter) + ']/div[11]'

    #adding stuff up

    try:
        while driver.find_element_by_xpath('//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]'):
            try:
                time.sleep(1)
                while True:
                    info = driver.find_element_by_xpath(index_string).text
                    if not info:
                        pass
                    else:
                        # negative clause (removable)
                        if float(info) < -3:
                            pass
                        else:
                            sum_yields = sum_yields + float(info)
                            valid_bond_counter = valid_bond_counter + 1
                    counter += 1
                    index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
                        str(counter) + ']/div[11]'
            except NoSuchElementException or StaleElementReferenceException:
                counter = 1
                index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
                    str(counter) + ']/div[11]'
            driver.find_element_by_class_name('qs-pageutil-next').click()
            # this sleep is needed for the information to load after pressing 'next'
            driver.implicitly_wait(1)
    except ElementNotVisibleException:
        driver.delete_all_cookies()
        driver.refresh()
    except NoSuchElementException:
        if valid_bond_counter == 0:
            sum_yields = 0
            valid_bond_counter = 1

    average_yield = sum_yields / valid_bond_counter
    return average_yield


def get_mv_debt(stock):

    # not great way of doing it... using beautiful soup
    # url = "https://finance.yahoo.com/quote/"+stock+"/balance-sheet?p="+stock
    # # pattern = re.compile('Short/Current Long Term Debt')
    # source = urllib.request.urlopen(url).read()
    # soup = bs.BeautifulSoup(source, 'lxml')
    #
    # table = soup.table
    # table = soup.find('table')
    # table_rows = table.find_all('tr')
    # for tr in table_rows:
    #     td = tr.find_all('td')
    #     row = [i.text for i in td]
    #     print(row)
    #

    # finding average price:

    driver = webdriver.Chrome()
    driver.get("http://finra-markets.morningstar.com/MarketData/CompanyInfo/default.jsp")
    driver.implicitly_wait(1)
    # search the company
    text_box = driver.find_element_by_id("ms-finra-autocomplete-box")
    text_box.send_keys(stock)
    time.sleep(1)
    driver.find_element_by_css_selector(".button_blue.autocomplete-go").click()
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@id="ms-equity-detail"]/div/div/div[1]/div[1]/div/div[1]/div[2]/ul/li[4]').click()
    driver.implicitly_wait(1)
    driver.find_element_by_class_name("ms-finra-more-bond").click()
    driver.implicitly_wait(1)
    driver.find_element_by_css_selector(".button_blue.agree").click()

    # average counter
    sum_prices = 0.0
    counter = 1
    valid_bond_counter = 0
    index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
                   str(counter) + ']/div[10]'

    # adding stuff up
    try:
        while driver.find_element_by_xpath('//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]'):
            try:
                time.sleep(1)
                while True:
                    info = driver.find_element_by_xpath(index_string).text
                    if not info:
                        pass
                    else:
                        # negative clause (removable)
                        if float(info) < -3:
                            pass
                        else:
                            sum_prices = sum_prices + float(info)
                            valid_bond_counter = valid_bond_counter + 1
                    counter += 1
                    index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
                                   str(counter) + ']/div[10]'
            except NoSuchElementException:
                counter = 1
                index_string = '//*[@id="ms-finra-search-results"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[' + \
                               str(counter) + ']/div[10]'
            driver.find_element_by_class_name('qs-pageutil-next').click()
            # this sleep is needed for the information to load after pressing 'next'
            driver.implicitly_wait(1)
    except ElementNotVisibleException:
        driver.delete_all_cookies()
        driver.refresh()
    except NoSuchElementException:
        if valid_bond_counter == 0:
            sum_prices = 0
            valid_bond_counter = 1

    average_price = sum_prices / valid_bond_counter

    # getting debt from yahoo finance
    dfs = pd.read_html('https://finance.yahoo.com/quote/'+stock+'/balance-sheet?p='+stock)
    df = dfs[0]
    std_cpltd = 0.0
    ltd = 0.0
    for index, row in df.iterrows():
        if row[0] == 'Short/Current Long Term Debt':
            if row[1] != '-':
                std_cpltd = row[1]
            else:
                pass
        if row[0] == 'Long Term Debt':
            if row[1] != '-':
                ltd = row[1]
            else:
                pass
    if std_cpltd == 0 and ltd == 0:
        print('Company has no material debt')
    else:
        mv_debt_mils = (float(std_cpltd)+(float(ltd)*float(average_price)/100.0))/1000.0
        return mv_debt_mils


def get_tax(stock):
    dfs = pd.read_html('https://finance.yahoo.com/quote/' + stock + '/financials?p=' + stock)
    df = dfs[0]
    ibt = 0.0
    ite = 0.0
    for index, row in df.iterrows():
        if row[0] == 'Income Before Tax':
            if row[1] != '-':
                ibt = row[1]
            elif row[2] != '-':
                ibt = row[2]
            elif row[3] != '-':
                ibt = row[3]
            else:
                pass
        if row[0] == 'Income Tax Expense':
            if row[1] != '-':
                ite = row[1]
            elif row[2] != '-':
                ite = row[2]
            elif row[3] != '-':
                ite = row[3]
            else:
                pass
    if ite == 0 or ibt == 0:
        print('Something is wrong, company income information is off')
    else:
        tax = float(ite)/float(ibt)
        return tax

