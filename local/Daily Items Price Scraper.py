import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
from tqdm import tqdm
import time

keys = [
    'Operation Wildfire Case Key',
    'Prisma Case Key',
    'Danger Zone Case Key',
    'Revolver Case Key',
    'eSports Key',
    'Huntsman Case Key',
    'Glove Case Key',
    'Operation Vanguard Case Key',
    'Spectrum Case Key',
    'Operation Hydra Case Key',
    'CS:GO Capsule Key',
    'Falchion Case Key',
    'Chroma 3 Case Key',
    'Clutch Case Key',
    'CS20 Case Key',
    'Operation Phoenix Case Key',
    'Community Sticker Capsule 1 Key',
    'Chroma Case Key',
    'CS:GO Case Key',
    'Winter Offensive Case Key',
    'Shadow Case Key',
    'Operation Breakout Case Key',
    'Chroma 2 Case Key',
    'Spectrum 2 Case Key',
    'Gamma 2 Case Key',
    'Gamma Case Key',
    'Horizon Case Key',
]

passes = [
    'Operation Broken Fang Premium Pass',
    'Berlin 2019 Viewer Pass',
    'Operation Hydra Access Pass',
    'Operation Bloodhound Access Pass',
    'Antwerp 2022 Viewer Pass',
    'Operation Breakout All Access Pass',
    'Katowice 2019 Viewer Pass',
    'Operation Shattered Web Premium Pass',
    'Operation Riptide Premium Pass',
    'Rio 2022 Viewer Pass',
    'Operation Phoenix Pass',
    'Operation Payback Pass',
    'Operation Bravo Pass',
    'Antwerp 2022 Viewer Pass + 3 Souvenir Tokens',
    'Operation Wildfire Access Pass',
    'Stockholm 2021 Viewer Pass',
    'Stockholm 2021 Viewer Pass + 3 Souvenir Tokens',
    'Operation Vanguard Access Pass',
    'Berlin 2019 Viewer Pass + 3 Souvenir Tokens',
    'Rio 2022 Viewer Pass + 3 Souvenir Tokens',
]

# pins = [
#     'Canals Pin',
#     'Guardian 3 Pin',
#     'Death Sentence Pin',
#     'Welcome to the Clutch Pin',
#     'Inferno 2 Pin',
#     'Guardian 2 Pin',
#     'Wildfire Pin',
#     'City 17 Pin',
#     'Bloodhound Pin',
#     'Train Pin',
#     'Guardian Pin',
#     'Brigadier General Pin',
#     'Hydra Pin',
#     'Phoenix Pin',
#     'Tactics Pin',
#     'Lambda Pin',
#     'Overpass Pin',
#     'Baggage Pin',
#     'Easy Peasy Pin',
#     'Victory Pin',
#     'Sustenance! Pin',
#     'Combine Helmet Pin',
#     'Nuke Pin',
#     'Headcrab Grab Pin',
#     'Copper Lambda Pin',
#     'Office Pin',
#     'Bravo Pin',
#     'CMB Pin',
#     'Inferno Pin',
#     'Cobblestone Pin',
#     'Aces High Pin',
#     'Black Mesa Pin',
#     'Cache Pin',
#     'Guardian Elite Pin',
#     'Chroma Pin',
#     'Howl Pin',
#     'Vortigaunt Pin',
#     'Civil Protection Pin',
#     'Valeria Pheonix Pin',
#     'Mirage Pin',
#     'Health Pin',
#     'Italy Pin',
#     'Alyx Pin',
#     'Dust II Pin',
#     'Militia Pin',
# ]

# nuke = [
#     'Antwerp 2022 Nuke Souvenir Package',
#     'Berlin 2019 Nuke Souvenir Package',
#     'Stockholm 2021 Nuke Souvenir Package',
#     'Rio 2022 Nuke Souvenir Package',
#     'London 2018 Nuke Souvenir Package',
#     'Katowice 2019 Nuke Souvenir Package',
#     'Atlanta 2017 Nuke Souvenir Package',
#     'Cologne 2016 Nuke Souvenir Package',
#     'Boston 2018 Nuke Souvenir Package',
#     'Krakow 2017 Nuke Souvenir Package',
#     'MLG Columbus 2016 Nuke Souvenir Package',
#     'ESL One Cologne 2014 Nuke Souvenir Package',
#     'ESL One Katowice 2015 Nuke Souvenir Package',
#     'DreamHack 2014 Nuke Souvenir Package',
# ]
#
# train = [
#     'London 2018 Train Souvenir Package',
#     'Katowice 2019 Train Souvenir Package',
#     'Krakow 2017 Train Souvenir Package',
#     'Berlin 2019 Train Souvenir Package',
#     'Atlanta 2017 Train Souvenir Package',
#     'Boston 2018 Train Souvenir Package',
#     'Cologne 2016 Train Souvenir Package',
#     'ESL One Cologne 2015 Train Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Train Souvenir Package',
#     'MLG Columbus 2016 Train Souvenir Package',
# ]
#
# mirage = [
#     'Stockholm 2021 Mirage Souvenir Package',
#     'Rio 2022 Mirage Souvenir Package',
#     'Antwerp 2022 Mirage Souvenir Package',
#     'London 2018 Mirage Souvenir Package',
#     'Boston 2018 Mirage Souvenir Package',
#     'Berlin 2019 Mirage Souvenir Package',
#     'Katowice 2019 Mirage Souvenir Package',
#     'ESL One Cologne 2015 Mirage Souvenir Package',
#     'Krakow 2017 Mirage Souvenir Package',
#     'MLG Columbus 2016 Mirage Souvenir Package',
#     'Cologne 2016 Mirage Souvenir Package',
#     'Atlanta 2017 Mirage Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Mirage Souvenir Package',
#     'ESL One Katowice 2015 Mirage Souvenir Package',
#     'ESL One Cologne 2014 Mirage Souvenir Package',
#     'DreamHack 2014 Mirage Souvenir Package',
# ]
#
# overpass = [
#     'Rio 2022 Overpass Souvenir Package',
#     'Antwerp 2022 Overpass Souvenir Package',
#     'London 2018 Overpass Souvenir Package',
#     'Berlin 2019 Overpass Souvenir Package',
#     'Stockholm 2021 Overpass Souvenir Package',
#     'Katowice 2019 Overpass Souvenir Package',
#     'Boston 2018 Overpass Souvenir Package',
#     'Atlanta 2017 Overpass Souvenir Package',
#     'ESL One Cologne 2015 Overpass Souvenir Package',
#     'Krakow 2017 Overpass Souvenir Package',
#     'MLG Columbus 2016 Overpass Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Overpass Souvenir Package',
#     'Cologne 2016 Overpass Souvenir Package',
#     'ESL One Katowice 2015 Overpass Souvenir Package',
#     'ESL One Cologne 2014 Overpass Souvenir Package',
#     'DreamHack 2014 Overpass Souvenir Package',
# ]
#
# inferno = [
#     'Antwerp 2022 Inferno Souvenir Package',
#     'Rio 2022 Inferno Souvenir Package',
#     'Stockholm 2021 Inferno Souvenir Package',
#     'Katowice 2019 Inferno Souvenir Package',
#     'London 2018 Inferno Souvenir Package',
#     'Berlin 2019 Inferno Souvenir Package',
#     'Boston 2018 Inferno Souvenir Package',
#     'Krakow 2017 Inferno Souvenir Package',
#     'ESL One Cologne 2015 Inferno Souvenir Package',
#     'MLG Columbus 2016 Inferno Souvenir Package',
#     'ESL One Katowice 2015 Inferno Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Inferno Souvenir Package',
#     'ESL One Cologne 2014 Inferno Souvenir Package',
#     'DreamHack 2014 Inferno Souvenir Package',
# ]
#
# cobblestone = [
#     'Boston 2018 Cobblestone Souvenir Package',
#     'ESL One Cologne 2015 Cobblestone Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Cobblestone Souvenir Package',
#     'Krakow 2017 Cobblestone Souvenir Package',
#     'Atlanta 2017 Cobblestone Souvenir Package',
#     'Cologne 2016 Cobblestone Souvenir Package',
#     'ESL One Katowice 2015 Cobblestone Souvenir Package',
#     'MLG Columbus 2016 Cobblestone Souvenir Package',
#     'ESL One Cologne 2014 Cobblestone Souvenir Package',
# ]
#
# cache = [
#     'Katowice 2019 Cache Souvenir Package',
#     'London 2018 Cache Souvenir Package',
#     'Boston 2018 Cache Souvenir Package',
#     'Atlanta 2017 Cache Souvenir Package',
#     'MLG Columbus 2016 Cache Souvenir Package',
#     'Krakow 2017 Cache Souvenir Package',
#     'ESL One Cologne 2015 Cache Souvenir Package',
#     'Cologne 2016 Cache Souvenir Package',
#     'ESL One Katowice 2015 Cache Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Cache Souvenir Package',
#     'DreamHack 2014 Cache Souvenir Package',
#     'ESL One Cologne 2014 Cache Souvenir Package',
# ]
#
# ancient = [
#     'Rio 2022 Ancient Souvenir Package',
#     'Stockholm 2021 Ancient Souvenir Package',
#     'Antwerp 2022 Ancient Souvenir Package',
# ]
#
# vertigo = [
#     'Stockholm 2021 Vertigo Souvenir Package',
#     'Berlin 2019 Vertigo Souvenir Package',
#     'Rio 2022 Vertigo Souvenir Package',
#     'Antwerp 2022 Vertigo Souvenir Package',
# ]
#
# dust2 = [
#     'Rio 2022 Dust II Souvenir Package',
#     'Stockholm 2021 Dust II Souvenir Package',
#     'Antwerp 2022 Dust II Souvenir Package',
#     'Berlin 2019 Dust II Souvenir Package',
#     'London 2018 Dust II Souvenir Package',
#     'Katowice 2019 Dust II Souvenir Package',
#     'ESL One Cologne 2015 Dust II Souvenir Package',
#     'DreamHack Cluj-Napoca 2015 Dust II Souvenir Package',
#     'Atlanta 2017 Dust II Souvenir Package',
#     'ESL One Katowice 2015 Dust II Souvenir Package',
#     'Cologne 2016 Dust II Souvenir Package',
#     'MLG Columbus 2016 Dust II Souvenir Package',
#     'ESL One Cologne 2014 Dust II Souvenir Package',
#     'DreamHack 2014 Dust II Souvenir Package',
# ]

souviners = [
    'Rio 2022 Dust II Souvenir Package',
    'Stockholm 2021 Dust II Souvenir Package',
    'Antwerp 2022 Dust II Souvenir Package',
    'Berlin 2019 Dust II Souvenir Package',
    'London 2018 Dust II Souvenir Package',
    'Katowice 2019 Dust II Souvenir Package',
    'ESL One Cologne 2015 Dust II Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Dust II Souvenir Package',
    'Atlanta 2017 Dust II Souvenir Package',
    'ESL One Katowice 2015 Dust II Souvenir Package',
    'Cologne 2016 Dust II Souvenir Package',
    'MLG Columbus 2016 Dust II Souvenir Package',
    'ESL One Cologne 2014 Dust II Souvenir Package',
    'DreamHack 2014 Dust II Souvenir Package',
    'Stockholm 2021 Vertigo Souvenir Package',
    'Berlin 2019 Vertigo Souvenir Package',
    'Rio 2022 Vertigo Souvenir Package',
    'Antwerp 2022 Vertigo Souvenir Package',
    'Rio 2022 Ancient Souvenir Package',
    'Stockholm 2021 Ancient Souvenir Package',
    'Antwerp 2022 Ancient Souvenir Package',
    'Katowice 2019 Cache Souvenir Package',
    'London 2018 Cache Souvenir Package',
    'Boston 2018 Cache Souvenir Package',
    'Atlanta 2017 Cache Souvenir Package',
    'MLG Columbus 2016 Cache Souvenir Package',
    'Krakow 2017 Cache Souvenir Package',
    'ESL One Cologne 2015 Cache Souvenir Package',
    'Cologne 2016 Cache Souvenir Package',
    'ESL One Katowice 2015 Cache Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Cache Souvenir Package',
    'DreamHack 2014 Cache Souvenir Package',
    'ESL One Cologne 2014 Cache Souvenir Package',
    'Boston 2018 Cobblestone Souvenir Package',
    'ESL One Cologne 2015 Cobblestone Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Cobblestone Souvenir Package',
    'Krakow 2017 Cobblestone Souvenir Package',
    'Atlanta 2017 Cobblestone Souvenir Package',
    'Cologne 2016 Cobblestone Souvenir Package',
    'ESL One Katowice 2015 Cobblestone Souvenir Package',
    'MLG Columbus 2016 Cobblestone Souvenir Package',
    'ESL One Cologne 2014 Cobblestone Souvenir Package',
    'Antwerp 2022 Inferno Souvenir Package',
    'Rio 2022 Inferno Souvenir Package',
    'Stockholm 2021 Inferno Souvenir Package',
    'Katowice 2019 Inferno Souvenir Package',
    'London 2018 Inferno Souvenir Package',
    'Berlin 2019 Inferno Souvenir Package',
    'Boston 2018 Inferno Souvenir Package',
    'Krakow 2017 Inferno Souvenir Package',
    'ESL One Cologne 2015 Inferno Souvenir Package',
    'MLG Columbus 2016 Inferno Souvenir Package',
    'ESL One Katowice 2015 Inferno Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Inferno Souvenir Package',
    'ESL One Cologne 2014 Inferno Souvenir Package',
    'DreamHack 2014 Inferno Souvenir Package',
    'Rio 2022 Overpass Souvenir Package',
    'Antwerp 2022 Overpass Souvenir Package',
    'London 2018 Overpass Souvenir Package',
    'Berlin 2019 Overpass Souvenir Package',
    'Stockholm 2021 Overpass Souvenir Package',
    'Katowice 2019 Overpass Souvenir Package',
    'Boston 2018 Overpass Souvenir Package',
    'Atlanta 2017 Overpass Souvenir Package',
    'ESL One Cologne 2015 Overpass Souvenir Package',
    'Krakow 2017 Overpass Souvenir Package',
    'MLG Columbus 2016 Overpass Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Overpass Souvenir Package',
    'Cologne 2016 Overpass Souvenir Package',
    'ESL One Katowice 2015 Overpass Souvenir Package',
    'ESL One Cologne 2014 Overpass Souvenir Package',
    'DreamHack 2014 Overpass Souvenir Package',
    'Stockholm 2021 Mirage Souvenir Package',
    'Rio 2022 Mirage Souvenir Package',
    'Antwerp 2022 Mirage Souvenir Package',
    'London 2018 Mirage Souvenir Package',
    'Boston 2018 Mirage Souvenir Package',
    'Berlin 2019 Mirage Souvenir Package',
    'Katowice 2019 Mirage Souvenir Package',
    'ESL One Cologne 2015 Mirage Souvenir Package',
    'Krakow 2017 Mirage Souvenir Package',
    'MLG Columbus 2016 Mirage Souvenir Package',
    'Cologne 2016 Mirage Souvenir Package',
    'Atlanta 2017 Mirage Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Mirage Souvenir Package',
    'ESL One Katowice 2015 Mirage Souvenir Package',
    'ESL One Cologne 2014 Mirage Souvenir Package',
    'DreamHack 2014 Mirage Souvenir Package',
    'London 2018 Train Souvenir Package',
    'Katowice 2019 Train Souvenir Package',
    'Krakow 2017 Train Souvenir Package',
    'Berlin 2019 Train Souvenir Package',
    'Atlanta 2017 Train Souvenir Package',
    'Boston 2018 Train Souvenir Package',
    'Cologne 2016 Train Souvenir Package',
    'ESL One Cologne 2015 Train Souvenir Package',
    'DreamHack Cluj-Napoca 2015 Train Souvenir Package',
    'MLG Columbus 2016 Train Souvenir Package',
    'Antwerp 2022 Nuke Souvenir Package',
    'Berlin 2019 Nuke Souvenir Package',
    'Stockholm 2021 Nuke Souvenir Package',
    'Rio 2022 Nuke Souvenir Package',
    'London 2018 Nuke Souvenir Package',
    'Katowice 2019 Nuke Souvenir Package',
    'Atlanta 2017 Nuke Souvenir Package',
    'Cologne 2016 Nuke Souvenir Package',
    'Boston 2018 Nuke Souvenir Package',
    'Krakow 2017 Nuke Souvenir Package',
    'MLG Columbus 2016 Nuke Souvenir Package',
    'ESL One Cologne 2014 Nuke Souvenir Package',
    'ESL One Katowice 2015 Nuke Souvenir Package',
    'DreamHack 2014 Nuke Souvenir Package',
]

operations = [
    'Operation Bravo Case',
    'Operation Phoenix Weapon Case',
    'Operation Breakout Weapon Case',
    'Operation Vanguard Weapon Case',
    'Falchion Case',
    'Operation Wildfire Case',
    'Operation Hydra Case',
    'Shattered Web Case',
    'Operation Broken Fang Case',
    'Operation Riptide Case',
]

baseURL = 'https://steamcommunity.com/market/listings/730/'

def getSkinURLs(items, filename, timeout=15):
    combined = pd.DataFrame()
    for item in tqdm(items):
        time.sleep(timeout)
        url = baseURL + urllib.parse.quote(item)
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

        dataframe['price'] = dataframe['price'].astype(float)
        dataframe['volume'] = dataframe['volume'].astype(int)

        dataframe = dataframe.drop(columns=['volume'])

        dataframe = dataframe.rename(columns={'price': item})

        dataframe['date'] = dataframe['date'].str[:-4]
        dateFormat = "%b %d %Y %H"
        dataframe['date'] = pd.to_datetime(dataframe['date'], format=dateFormat)

        dataframe = dataframe[dataframe['date'] < pd.to_datetime('today') - pd.Timedelta('31 days')]

        dataframe = dataframe.set_index('date')

        # dataframe = dataframe.iloc[1:] #dont use for items with low volume like rare items

        combined = pd.concat([combined, dataframe], axis=1)

        # dataframe.to_csv(f'Data/Operation Cases/Keys/{item.replace(":", "-")}.csv', index=False)
        combined.to_csv('Data/Operation Cases/Portfolio/' + filename + '.csv')
        # '' + item + '.csv', index = False, errors = 'replace')

        print(combined)

# getSkinURLs(keys, 'Keys')
# getSkinURLs(passes, 'Passes')
# getSkinURLs(operations, 'Operations')
# getSkinURLs(overpass, 'Overpass')
# getSkinURLs(inferno, 'Inferno')
# getSkinURLs(cobblestone, 'Cobblestone')
# getSkinURLs(cache, 'Cache')
# getSkinURLs(ancient, 'Ancient')
# getSkinURLs(vertigo, 'Vertigo')
# getSkinURLs(dust2, 'Dust2')

# getSkinURLs(pins, 'Pins')
# getSkinURLs(souviners, 'Souviners')
