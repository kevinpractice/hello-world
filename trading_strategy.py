import pandas as pd
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import fix_yahoo_finance


start = datetime.datetime(2018, 1, 1)
end = datetime.datetime.today().strftime('%Y-%m-%d')
df= web.get_data_yahoo('AAPL', start, end)
df = pd.DataFrame(df)
rolling_mean = df['Open'].rolling(10).mean().dropna()
rolling_std = df['Open'].rolling(10).std().dropna()
df['high'] = rolling_mean.add(rolling_std)
df['low'] = rolling_mean.sub(rolling_std)
df = df.dropna()

import numpy as np
df['Position'] = None
df['Market_Return'] = None
for row in range(len(df)):
    
    if (df['Open'].iloc[row] > df['high'].iloc[row]) and (df['Open'].iloc[row-1] < df['high'].iloc[row-1]):
        df['Position'].iloc[row] = 1

    if (df['Open'].iloc[row] < df['low'].iloc[row]) and (df['Open'].iloc[row-1] > df['low'].iloc[row-1]):
        df['Position'].iloc[row] = -1
            

df['Position'].fillna(method='ffill',inplace=True)
df['Market_Return'] = np.log(df['Open'].div(df['Open'].shift(1)))
df['standard_V'] = rolling_std
df['Strategy_Return'] = df['Market_Return'].multiply(df['Position'])
df['signal'] = df['Position'].diff()
df['ratio'] = df['Strategy_Return'].div(df['standard_V'])
df.to_csv('/Users/wangkevin/Documents/trading.csv')