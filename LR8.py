... import time
... from dataclasses import dataclass
... from datetime import datetime, timedelta
... import pandas as pd
... from pandas_ta import rsi, adx, cci
... from binance import Client
... 
... API_KEY    = ""    
... API_SECRET = ""    
... ASSET      = "BTCUSDT"
... QUANTITY   = 0.001  
... 
... TP_PCT     = 0.05
... SL_PCT     = 0.02
... 
... client = Client(API_KEY, API_SECRET)
... 
... 
... @dataclass
... class Signal:
...     time: datetime
...     asset: str
...     quantity: float
...     side: str           
...     entry: float
...     take_profit: float
...     stop_loss: float
...     result: float = 0.0  
... 
... 
... class Strategy:
...     def __init__(self, asset: str, quantity: float):
...         self.asset = asset
...         self.quantity = quantity
... 
    def fetch_ohlcv(self, limit: int = 100) -> pd.DataFrame:
        now = datetime.utcnow()
        start = now - timedelta(minutes=limit)
        klines = client.get_historical_klines(
            symbol=self.asset,
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str=start.strftime("%Y-%m-%d %H:%M:%S"),
            end_str=now.strftime("%Y-%m-%d %H:%M:%S")
        )
        df = pd.DataFrame(klines, columns=[
            "open_time","open","high","low","close","volume",
            *range(6,12), "close_time", *range(13,20)
        ])
        df["time"]  = pd.to_datetime(df["open_time"], unit="ms")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        return df[["time", "close"]].set_index("time")

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["RSI"] = rsi(df["close"], length=14)
        cci_high = df["close"]  
        df["CCI"] = cci(high=df["close"], low=df["close"], close=df["close"], length=20)
        df["ADX"] = adx(high=df["close"], low=df["close"], close=df["close"], length=14)["ADX_14"]
        return df.dropna()

    def create_signal(self) -> Signal | None:
        df = self.fetch_ohlcv()
        df = self.compute_indicators(df)
        last = df.iloc[-1]

        rsi_val = last["RSI"]
        cci_val = last["CCI"]
        adx_val = last["ADX"]
        price   = last["close"]

        if (rsi_val < 30 or cci_val < -100) and adx_val > 35:
            side = "BUY"
        elif (rsi_val > 70 or cci_val > 100) and adx_val > 35:
            side = "SELL"
        else:
            return None

        if side == "BUY":
            tp = price * (1 + TP_PCT)
            sl = price * (1 - SL_PCT)
        else:
            tp = price * (1 - TP_PCT)
            sl = price * (1 + SL_PCT)

        return Signal(
            time=datetime.now(),
            asset=self.asset,
            quantity=self.quantity,
            side=side,
            entry=price,
            take_profit=round(tp, 2),
            stop_loss=round(sl, 2)
        )


def monitor(strategy: Strategy, interval: int = 60):
    print("[Monitor] Старт моніторингу стратегії…")
    while True:
        sig = strategy.create_signal()
        if sig:
            print(f"[{sig.time:%Y-%m-%d %H:%M:%S}] SIGNAL → {sig.side} {sig.asset} @ {sig.entry:.2f}")
            print(f"    TP: {sig.take_profit:.2f}, SL: {sig.stop_loss:.2f}")
        time.sleep(interval)


if __name__ == "__main__":
    strat = Strategy(asset=ASSET, quantity=QUANTITY)
    monitor(strat, interval=60)
