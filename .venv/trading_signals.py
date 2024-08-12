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

# Example usage
if __name__ == "__main__":
    symbols = ["AAPL", "GOOGL", "MSFT"]  # Aggiungi i simboli che desideri
    for symbol in symbols:
        df = pd.read_csv(f"{symbol}_trend.csv")
        signals = TradingSignals(df)
        df = signals.generate_signals()
        df.to_csv(f"{symbol}_signals.csv")
