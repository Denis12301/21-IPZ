from binance import Client
import pandas as pd
from datetime import datetime, timedelta

API_KEY = ""
API_SECRET = ""

client = Client(API_KEY, API_SECRET)

def calculate_rsi(series: pd.Series, period: int) -> pd.Series:
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    avg_gain = avg_gain.combine_first(
        gain.ewm(alpha=1/period, adjust=False).mean()
    )
    avg_loss = avg_loss.combine_first(
        loss.ewm(alpha=1/period, adjust=False).mean()
    )

    rs  = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_rsi(asset: str, periods: list[int]) -> pd.DataFrame:
... 
...     today_utc      = datetime.utcnow().date()
...     yesterday_utc  = today_utc - timedelta(days=1)
...     start_str = f"{yesterday_utc} 00:00:00"
...     end_str   = f"{today_utc} 00:00:00"
... 
...     klines = client.get_historical_klines(
...         symbol=asset,
...         interval=Client.KLINE_INTERVAL_1MINUTE,
...         start_str=start_str,
...         end_str=end_str
...     )
... 
...     df = pd.DataFrame(klines, columns=[
...         'open_time', 'open', 'high', 'low', 'close', 'volume',
...         *range(6,12), 'close_time', *range(13,20)
...     ])
...     df['time']  = pd.to_datetime(df['open_time'], unit='ms')
...     df['close'] = pd.to_numeric(df['close'], errors='coerce')
...     df = df[['time', 'close']].reset_index(drop=True)
... 
...     for p in periods:
...         df[f'RSI_{p}'] = calculate_rsi(df['close'], p)
... 
...     out_cols = ['time'] + [f'RSI_{p}' for p in periods]
...     result = df[out_cols].copy()
...     result.insert(0, 'index', result.index)
...     return result
... 
... if __name__ == "__main__":
...     periods = [14, 27, 100]
...     df_rsi = get_rsi("BTCUSDT", periods)
...     print(df_rsi.head(10))      
...     df_rsi.to_csv("rsi_1m_24h.csv", index=False)
