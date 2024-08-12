# data_fetcher.py
import requests
import pandas as pd

class DataFetcher:
    def __init__(self, symbols, access_token):
        self.symbols = symbols
        self.access_token = access_token

    def fetch_data(self):
        data = {}
        for symbol in self.symbols:
            url = f"https://api.schwabapi.com/v1/marketdata/{symbol}/quotes"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                df = pd.DataFrame(json_data)
                data[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return data
