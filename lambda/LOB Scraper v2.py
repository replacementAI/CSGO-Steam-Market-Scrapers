import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import time
import boto3
import os

s3 = boto3.client('s3')
os.chdir('/tmp')

def lambda_handler(event, context):
    URL = 'https://steamcommunity.com/market/listings/730/MAG-7%20%7C%20Insomnia%20%28Factory%20New%29' # CHANGE TO THE URL OF THE SKIN YOU WANT TO SCRAPE
  
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    variable = soup.find_all('script', type='text/javascript')[-1].text

    start = ' Market_LoadOrderSpread( '
    end = ' ); },'
    item_nameid = variable[(variable.find(start) + len(start)):variable.find(end, variable.find(start))]
  
  
    baseURL = 'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=' + item_nameid + '&two_factor=0' # DO NOT TOUCH
    
    filename = f'{time.strftime("%Y-%m-%d %H:%M", time.localtime())} revolution case.csv'
    
    dataframe = pd.DataFrame(columns=['date', 'buy_price', 'buy_volume', 'sell_price', 'sell_volume'])

    soup = BeautifulSoup(requests.get(baseURL).text, 'html.parser').text

    json_data = json.loads(soup)

    try:
        buy_order = json_data['buy_order_graph'][0]
        sell_order = json_data['sell_order_graph'][0]
    except TypeError:

        order_dict = {'date': time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                        'buy_price': 'NaN',
                        'buy_volume': 'NaN',
                        'sell_price': 'NaN',
                        'sell_volume': 'NaN',
                        }
        dataframe = dataframe.append(order_dict, ignore_index=True)

        return dataframe.to_csv(filename, index=False, header=True, mode='w')

    highest_buy_order = buy_order[:-1]
    lowest_sell_order = sell_order[:-1]

    order_dict = {'date': time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                  'buy_price': highest_buy_order[0],
                  'buy_volume': highest_buy_order[1],
                  'sell_price': lowest_sell_order[0],
                  'sell_volume': lowest_sell_order[1],
                  }
    dataframe = dataframe.append(order_dict, ignore_index=True)
    
    dataframe.to_csv(filename, index=False, header=True, mode='w')
    
    s3.upload_file(filename, os.environ['BUCKET_NAME'], filename)
