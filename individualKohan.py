>>> import pandas as pd
... import numpy as np
... import matplotlib.pyplot as plt
... from datetime import datetime
... 
... RANGE         = 15            
... SHOW_PDH_PDL  = False         
... SHOW_BEAR_BOS = False         
... SHOW_BULL_BOS = False         
... 
... BEAR_OB_COLOR   = (1.0, 0.0, 0.0, 0.4)  
... BULL_OB_COLOR   = (0.0, 1.0, 0.0, 0.4)
... BOS_LINE_COLOR  = {'bear': 'red', 'bull': 'green'}
... TREND_COLORS    = {'bull': 'lime', 'bear': 'red'}
... BOS_CANDLE_COLOR= 'yellow'
... 
... def compute_order_blocks(df: pd.DataFrame):
...     """
...     Вхід: df з колонками ['open','high','low','close'], індекс — datetime
...     Повертає:
...       - long_blocks  : list of dicts {left, right, top, bottom}
...       - short_blocks : list of dicts {left, right, top, bottom}
...       - bos_lines    : list of dicts {x0, y0, x1, y1, type}
...     """
...     long_blocks, short_blocks, bos_lines = [], [], []
... 
...     last_down_idx = last_up_idx = None
...     last_down     = last_low = None
...     last_up       = last_high = None
...     last_up_low   = last_up_open = None
... 
...     lows = df['low'].values
...     highs = df['high'].values
...     closes = df['close'].values
...     opens = df['open'].values
... 
...     n = len(df)
    for i in range(RANGE, n):
        struct_low = lows[i-RANGE:i].min()
        if closes[i] < opens[i]:
            last_down_idx = i
            last_low = lows[i]
        else:
            last_up_idx = i
            last_up = closes[i]
            last_up_low = lows[i]
            last_up_open = opens[i]
            last_high = highs[i]

        if closes[i] < struct_low and last_up_idx is not None and (i - last_up_idx) < 1000:
            short_blocks.append({
                'left':  last_up_idx,
                'right': i,
                'top':   last_high,
                'bottom': last_up_low,
                'color': BEAR_OB_COLOR
            })
            if SHOW_BEAR_BOS:
                bos_lines.append({
                    'x0': last_up_idx, 'y0': struct_low,
                    'x1': i,         'y1': struct_low,
                    'type': 'bear'
                })

        for j, box in enumerate(short_blocks[:]):
            if closes[i] > box['top']:
                short_blocks.pop(j)
                long_blocks.append({
                    'left':  box['left'],
                    'right': i,
                    'top':   box['top'],
                    'bottom': box['bottom'],
                    'color': BULL_OB_COLOR
                })
                if SHOW_BULL_BOS:
                    bos_lines.append({
                        'x0': box['left'], 'y0': box['top'],
                        'x1': i,          'y1': box['top'],
                        'type': 'bull'
                    })

    return long_blocks, short_blocks, bos_lines


def plot_order_blocks(df: pd.DataFrame, long_blocks, short_blocks, bos_lines):
    """
    Малює ціновий графік з накладеними блоками та BOS лініями.
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df.index, df['close'], color='black', linewidth=1, label='Close')

    for box in long_blocks + short_blocks:
        ax.add_patch(plt.Rectangle(
            (df.index[box['left']], box['bottom']),
            df.index[box['right']] - df.index[box['left']],
            box['top'] - box['bottom'],
            color=box['color']
        ))

    for line in bos_lines:
        ax.plot(
            [df.index[line['x0']], df.index[line['x1']]],
            [line['y0'], line['y1']],
            color=BOS_LINE_COLOR[line['type']],
            linestyle='--'
        )

    ax.set_title("Order Blocks Indicator")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    dates = pd.date_range(end=datetime.now(), periods=500, freq='T')
    np.random.seed(0)
    price = np.cumsum(np.random.randn(500)) + 100
    df = pd.DataFrame({
        'open':  price + np.random.randn(500)*0.5,
        'high':  price + np.random.rand(500),
        'low':   price - np.random.rand(500),
        'close': price
    }, index=dates)

    longs, shorts, bos = compute_order_blocks(df)
