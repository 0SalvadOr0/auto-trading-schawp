import pandas as pd

class TrendCalculator:
    def __init__(self, df):
        self.df = df

    def calculate_trend(self):
        self.df['Trend'] = self.df['Close'].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
        return self.df

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("AAPL.csv")
    calculator = TrendCalculator(df)
    df = calculator.calculate_trend()
    df.to_csv("AAPL_trend.csv")
