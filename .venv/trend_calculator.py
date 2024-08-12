import pandas as pd

class TrendCalculator:
    def __init__(self, df):
        self.df = df

    def calculate_trend(self):
        self.df['Trend'] = self.df['Close'].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
        return self.df
