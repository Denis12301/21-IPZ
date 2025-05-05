>>> import pandas as pd
... import matplotlib.pyplot as plt
... 
... INPUT_CSV  = "rsi_1m_24h.csv"   
... OUTPUT_IMG = "rsi_charts.png"
... 
... df = pd.read_csv(INPUT_CSV, parse_dates=['time'])
... 
... df = df.dropna(subset=['RSI_14', 'RSI_27', 'RSI_100'])
... 
... plots = {
...     'bar':     'RSI_27',   
...     'scatter': 'RSI_14',   
...     'plot':    'RSI_100'   
... }
... 
... plt.figure(figsize=(9, 3))
... 
... for idx, (kind, col) in enumerate(plots.items(), start=1):
...     ax = plt.subplot(1, 3, idx)
...     x = df['time']
...     y = df[col]
... 
...     if kind == 'bar':
...         ax.bar(x, y)
...     elif kind == 'scatter':
...         ax.scatter(x, y)
...     else:  
...         ax.plot(x, y)
... 
...     ax.set_title(f"{kind} - {col.replace('_',' ')}")
...     ax.set_xlabel("Time")
    ax.set_ylabel("RSI Value")
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45)
        lbl.set_ha('right')

plt.tight_layout()
plt.savefig(OUTPUT_IMG)
plt.show()

