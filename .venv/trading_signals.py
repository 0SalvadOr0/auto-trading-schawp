import pandas as pd

class TradingSignals:
    def __init__(self, df):
        self.df = df

    def generate_signals(self):
        self.df['BuySignal'] = (self.df['Trend'] == 1) & (self.df['Trend'].shift(1) == 1)
        self.df['SellSignal'] = (self.df['Trend'] == -1) & (self.df['Trend'].shift(1) == -1)
        self.df['BuyEntryPrice'] = self.df['Open'].shift(-1).where(self.df['BuySignal'])
        self.df['SellEntryPrice'] = self.df['Open'].shift(-1).where(self.df['SellSignal'])
        self.df['BuyOrder'] = self.df['BuyEntryPrice'].notna()
        self.df['SellOrder'] = self.df['SellEntryPrice'].notna()
        return self.df
