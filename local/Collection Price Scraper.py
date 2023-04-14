import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
from tqdm import tqdm
import time

def getSkinURLs(case):
    baseURL = 'https://steamcommunity.com/market/listings/730/'

    soup = BeautifulSoup(requests.get(baseURL + urllib.parse.quote(case)).text, 'html.parser')
    variable = soup.find_all('script', type='text/javascript')[-1].text

    start = '[{'
    end = '}]'
    data = variable[(variable.find(start)):(variable.find(end, (variable.find(start))) + len(end))]
    json_data = json.loads(data)

    items = []
    for item in json_data:
        if 'color' in item:
            items.append(item['value'])

    skins = items[1:-2]
    encodedSkins = [urllib.parse.quote(skin) for skin in skins]

    wears = ['Factory%20New', 'Minimal%20Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
    statTrak = 'StatTrak™%20'
    skinURLs = []
    for skin in encodedSkins:
        for wear in wears:
            url = baseURL + skin + '%20%28' + wear + '%29'
            skinURLs.append(url)
            url = baseURL + statTrak + skin + '%20%28' + wear + '%29'
            skinURLs.append(url)

    return skinURLs

def getSkinData(URLs, timeout=14):
    for url in tqdm(URLs):
        time.sleep(timeout)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        variable = soup.find_all('script', type='text/javascript')[-1].text

        start = '[["'
        end = '"]]'
        data = variable[(variable.find(start)):(variable.find(end, (variable.find(start))) + len(end))]
        try:
            data = json.loads(data)

        except json.decoder.JSONDecodeError:
            continue

        dataframe = pd.DataFrame(data, columns=['date', 'price', 'volume'])

        dataframe['date'] = dataframe['date'].str[:-4]
        dateFormat = "%b %d %Y %H"
        dataframe['date'] = pd.to_datetime(dataframe['date'], format=dateFormat)

        dataframe['price'] = dataframe['price'].astype(float)
        dataframe['volume'] = dataframe['volume'].astype(int)

        dataframe.to_csv(urllib.parse.unquote(url.split('/')[-1]).replace('|', '_') + '.csv', index=False)

        print(urllib.parse.unquote(url.split('/')[-1]))

skinURLs = getSkinURLs('Revolution Case')
getSkinData(skinURLs)
