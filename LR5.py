>>> import pandas as pd
... from pandas_ta import rsi, cci, macd
... from datetime import datetime
... 
... INPUT_CSV  = "price_data.csv"              
... OUTPUT_CSV = "indicators_analysis.csv"     
... 
... def load_price_data(path: str) -> pd.DataFrame:
...     df = pd.read_csv(path, parse_dates=['Date'])
...     df.set_index('Date', inplace=True)
...     return df
... 
... def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
...     df['rsi'] = rsi(df['Close'], length=14)
...     df['cci'] = cci(high=df['High'], low=df['Low'], close=df['Close'], length=20)
...     macd_df = macd(close=df['Close'], fast=12, slow=26, signal=9)
...     df['macd'] = macd_df.iloc[:, 0]
...     return df
... 
... def decide_meaning(row: pd.Series) -> str:
...     buy  = (row['rsi'] < 30) | (row['cci'] < -100) | (row['macd'] > 0)
...     sell = (row['rsi'] > 70) | (row['cci'] > 100)  | (row['macd'] < 0)
...     if buy and not sell:
...         return "ціна буде рости"
...     if sell and not buy:
...         return "ціна буде падати"
...     return "ціна не зміниться"
... 
... def build_report(df: pd.DataFrame) -> pd.DataFrame:
...     report = df[['rsi', 'cci', 'macd']].dropna().copy()
...     report['meaning'] = report.apply(decide_meaning, axis=1)
...     return report.reset_index(drop=True)[['meaning', 'rsi', 'cci', 'macd']]
... 
... def main():
    df = load_price_data(INPUT_CSV)
    df = compute_indicators(df)
    report = build_report(df)
    report.to_csv(OUTPUT_CSV, index=False)
    print(f"[OK] Збережено {OUTPUT_CSV} — {len(report)} рядків, останній сигнал:")
    print(report.tail(1).to_dict(orient='records')[0])

if __name__ == "__main__":
