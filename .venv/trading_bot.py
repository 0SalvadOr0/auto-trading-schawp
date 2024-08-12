import os
import base64
import requests
import webbrowser
from loguru import logger
import pandas as pd
from data_fetcher import DataFetcher
from trend_calculator import TrendCalculator
from trading_signals import TradingSignals

class TradingBot:
    def __init__(self, symbols):
        self.symbols = symbols

    def construct_init_auth_url(self):
        app_key = "7K4OGus81oiQTwwOGTSWMMi7II3a5AOK"
        app_secret = "DyYTqL4cWdLuPEHH"
        auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={app_key}&redirect_uri=http://www.floridakeysvillas.com"
        logger.info("Click to authenticate:")
        logger.info(auth_url)
        return app_key, app_secret, auth_url

    def construct_headers_and_payload(self, returned_url, app_key, app_secret):
        response_code = f"{returned_url[returned_url.index('code=') + 5: returned_url.index('%40')]}@"
        credentials = f"{app_key}:{app_secret}"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "grant_type": "authorization_code",
            "code": response_code,
            "redirect_uri": " http://www.floridakeysvillas.com",
        }
        return headers, payload

    def retrieve_tokens(self, headers, payload):
        init_token_response = requests.post(
            url="https://api.schwabapi.com/v1/oauth/token",
            headers=headers,
            data=payload,
        )
        init_tokens_dict = init_token_response.json()
        return init_tokens_dict

    def place_order(self, symbol, quantity, order_type, access_token):
        account_id = "YOUR_ACCOUNT_ID"
        url = f"https://api.schwabapi.com/v1/accounts/{account_id}/orders"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        order = {
            "orderType": order_type,
            "quantity": quantity,
            "symbol": symbol,
            "priceType": "MARKET",
            "duration": "DAY"
        }
        response = requests.post(url, headers=headers, json=order)
        if response.status_code == 201:
            logger.info(f"Order placed successfully for {symbol}")
        else:
            logger.error(f"Failed to place order for {symbol}: {response.text}")

    def run(self):
        app_key, app_secret, cs_auth_url = self.construct_init_auth_url()
        webbrowser.open(cs_auth_url)
        logger.info("Paste Returned URL:")
        returned_url = input()
        init_token_headers, init_token_payload = self.construct_headers_and_payload(
            returned_url, app_key, app_secret
        )
        init_tokens_dict = self.retrieve_tokens(
            headers=init_token_headers, payload=init_token_payload
        )
        logger.debug(init_tokens_dict)

        access_token = init_tokens_dict['access_token']
        fetcher = DataFetcher(self.symbols, access_token)
        data = fetcher.fetch_data()
        for symbol, df in data.items():
            calculator = TrendCalculator(df)
            df = calculator.calculate_trend()
            signals = TradingSignals(df)
            df = signals.generate_signals()
            df.to_csv(f"{symbol}_signals.csv")

            # Place buy/sell orders based on signals
            for index, row in df.iterrows():
                if row['BuyOrder']:
                    self.place_order(symbol, 10, "BUY", access_token)
                elif row['SellOrder']:
                    self.place_order(symbol, 10, "SELL", access_token)

        return "Done!"

# Example usage
if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "GOOGL"]
    bot = TradingBot(symbols)
    bot.run()