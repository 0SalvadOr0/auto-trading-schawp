import requests
import pandas as pd
from loguru import logger

class DataFetcher:
    def __init__(self, access_token):
        self.access_token = access_token

    def fetch_data(self, symbols):
        data = {}
        for symbol in symbols:
            url = f"https://api.schwabapi.com/v1/marketdata/{symbol}/quotes"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    df = pd.DataFrame([json_data])  # Assicurati che json_data sia in un formato accettabile
                    data[symbol] = df
                except ValueError as e:
                    logger.error(f"Errore nel parsing dei dati per {symbol}: {e}")
            else:
                logger.error(f"Failed to fetch data for {symbol}: {response.status_code} - {response.text}")
        return data
