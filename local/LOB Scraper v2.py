import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import time

def get_item_nameid(URL):
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    variable = soup.find_all('script', type='text/javascript')[-1].text

    start = ' Market_LoadOrderSpread( '
    end = ' ); },'
    item_nameid = variable[(variable.find(start) + len(start)):variable.find(end, variable.find(start))]

    return item_nameid

def scrape(URL, dataframe, timeout=600):
    item_nameid = get_item_nameid(URL)

    baseURL = 'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=' + item_nameid + '&two_factor=0'

    time.sleep(timeout)

    soup = BeautifulSoup(requests.get(baseURL).text, 'html.parser').text

    json_data = json.loads(soup)

    try:
        buy_order = json_data['buy_order_graph'][0]
        sell_order = json_data['sell_order_graph'][0]
    except TypeError:

        order_dict = {'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                      'buy_price': 'NaN',
                      'buy_volume': 'NaN',
                      'sell_price': 'NaN',
                      'sell_volume': 'NaN',
                      }
        dataframe = dataframe.append(order_dict, ignore_index=True)

        return dataframe

    highest_buy_order = buy_order[:-1]
    lowest_sell_order = sell_order[:-1]

    order_dict = {'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                  'buy_price': highest_buy_order[0],
                  'buy_volume': highest_buy_order[1],
                  'sell_price': lowest_sell_order[0],
                  'sell_volume': lowest_sell_order[1],
                  }
    dataframe = dataframe.append(order_dict, ignore_index=True)

    dataframe.to_csv('10 minute revolution case.csv', index=False, header=False, mode='w')

    print(dataframe)

dataframe = pd.DataFrame(columns=['date', 'buy_price', 'buy_volume', 'sell_price', 'sell_volume'])

URL = 'https://steamcommunity.com/market/listings/730/MAG-7%20%7C%20Insomnia%20%28Factory%20New%29' #change this to the URL you wanna scrape

scrape(URL, dataframe)
