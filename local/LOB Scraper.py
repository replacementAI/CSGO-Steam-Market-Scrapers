import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import time

dataframe = pd.DataFrame(columns=['date', 'buy_price', 'buy_volume', 'sell_price', 'sell_volume'])

def getSkinURLs(URL, dataframe, timeout=600):
    while True:
        time.sleep(timeout)

        soup = BeautifulSoup(requests.get(URL).text, 'html.parser').text

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

            continue

        highest_buy_order = buy_order[:-1]
        lowest_sell_order = sell_order[:-1]

        order_dict = {'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                      'buy_price': highest_buy_order[0],
                      'buy_volume': highest_buy_order[1],
                      'sell_price': lowest_sell_order[0],
                      'sell_volume': lowest_sell_order[1],
                      }
        dataframe = dataframe.append(order_dict, ignore_index=True)

        dataframe.to_csv('scraped lob.csv', index=False, header=False, mode='w')

        print(dataframe)

URL = 'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=176358765&two_factor=0'
# replace item_nameid

getSkinURLs(URL, dataframe)
