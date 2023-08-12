import os
import requests
import pandas as pd

def load_one():

    r = requests.get('https://free-proxy-list.net/')


    df = pd.read_html(r.text)[0]

    df['IP Address'] = df['IP Address'].apply(lambda x: str(x))
    df['Port'] = df['Port'].apply(lambda x: str(x))

    df.to_csv('load_file/proxy.csv')

    #-----------------------------------------------

    df = pd.read_csv('load_file/proxy.csv')

    df['IP Address'] = df['IP Address'].apply(lambda x: str(x))
    df['Port'] = df['Port'].apply(lambda x: str(x))

    proxies = pd.DataFrame()

    proxies['proxy'] = df['IP Address'].astype(str) + ":" + df['Port'].astype(str)
    proxies['https'] = df['Https']

    os.remove('load_file/proxy.csv')
    proxies.to_csv('load_file/ip-port.csv')
