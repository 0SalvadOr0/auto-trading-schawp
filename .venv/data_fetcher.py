import requests
import pandas as pd
from loguru import logger

class DataFetcher:
    def __init__(self, refresh_access_token):
        self.access_token = refresh_access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def fetch_data(self, exchange):
        response = requests.get(
            url=f"https://api.schwabapi.com/marketdata/v1/{exchange}",
            headers=self.headers
        )

        if response.status_code == 200:
            response_data = response.json()
            response_frame = pd.DataFrame(response_data)
            screeners_frame = pd.json_normalize(
                response_frame["screeners"]
            )
            return screeners_frame
        elif response.status_code == 201:
            logger.info(response.text)
            logger.info("New resource created")
        else:
            logger.error(f"Error response with: {response.text}")
            logger.error(f"Code error: {response.status_code}")
            return None

