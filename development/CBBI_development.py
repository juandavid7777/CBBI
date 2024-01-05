import requests

import pandas as pd
import numpy as np

import httpx
from httpx import Client, Timeout

#----------------------------------------------------------------------
pd.options.plotting.backend = "plotly"

#----------------------------------------------------------------------
HTTP_TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'

HTTP = Client(
    headers={'User-Agent': USER_AGENT},
    timeout=Timeout(HTTP_TIMEOUT),
    follow_redirects=True,
    http1=True,
    http2=True,
)

#----------------------------------------------------------------------
response = HTTP.get('https://colintalkscrypto.com/cbbi/data/latest.json')
response.raise_for_status()
response_data = response.json()

df = pd.DataFrame.from_dict(response_data, orient='columns')
df.index = pd.to_datetime(df.index, unit='s')

df

#----------------------------------------------------------------------
response = httpx.get('https://colintalkscrypto.com/cbbi/data/latest.json')
response.raise_for_status()
response_data = response.json()

df = pd.DataFrame.from_dict(response_data, orient='columns')
df.index = pd.to_datetime(df.index, unit='s')

df

#----------------------------------------------------------------------
df.drop(columns = ["Price"]).plot()


#----------------------------------------------------------------------
def cs_fetch(path: str, data_selector: str, col_name: str) -> pd.DataFrame:
    response = HTTP.get(f'https://coinsoto.com/indicatorapi/{path}')
    response.raise_for_status()
    data = response.json()['data']

    if 'timeList' not in data and 'line' in data:
        data = data['line']

    data_x = data['timeList']
    data_y = data[data_selector]
    assert len(data_x) == len(data_y), f'{len(data_x)=} != {len(data_y)=}'

    df = pd.DataFrame({
        'Date': data_x[:len(data_y)],
        col_name: data_y,
    })

    df['Date'] = pd.to_datetime(df['Date'], unit='ms').dt.tz_localize(None)

    return df

# Example cs_fetch ---------------------------------------------------
df = cs_fetch(
            path='chain/index/charts?type=/charts/mvrv-zscore/',
            data_selector='value4',
            col_name='MVRV'
).set_index("Date")

df.plot(log_y = False)