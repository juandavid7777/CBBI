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