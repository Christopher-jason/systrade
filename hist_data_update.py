import config
import pandas as pd 
from datetime import datetime as dt
from datetime import timedelta


from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

tmp_df = pd.read_csv('Hist_data_TSLA.csv')
last_entry = tmp_df.tail(1)['timestamp'].values[0]
last_date = pd.to_datetime(last_entry).date()
start_date = last_date + timedelta(days=1)

end_date = dt.now().strftime('%Y-%m-%d')


stock_data_client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)

# Get last data
latest_hist_data = StockBarsRequest(
    symbol_or_symbols= ["TSLA"],
    timeframe=TimeFrame.Hour,
    start=start_date,
    end=end_date
)

tsla_bars = stock_data_client.get_stock_bars(latest_hist_data)

# Convert to dataframe
tsla_data = tsla_bars.df


tsla_data.to_csv('Hist_data_TSLA.csv', mode='a', header=not pd.read_csv('Hist_data_TSLA.csv').shape[0])


print("Remaining data collected.")