import alpaca_trade_api as tradeapi
from alpaca_trade_api import Stream
from alpaca_trade_api.common import URL
import pandas as pd
import schedule
import time
import threading
import config
from datetime import datetime

# Set your Alpaca API key and secret key here
API_KEY = config.API_KEY
API_SECRET = config.SECRET_KEY
BASE_URL = 'wss://stream.data.alpaca.markets/v2/iex'  # Adjust if necessary

# Initialize DataFrame from historical data and drop specified columns
df = pd.read_csv('Hist_data_TSLA.csv')
df = df.drop(columns=['trade_count', 'vwap'])

# Asynchronous function to handle incoming bar data
async def bar_handler(bar):
    global df
    # Check if the timestamp matches the full hour
    timestamp = pd.to_datetime(bar.t)
    if timestamp.minute == 0 and timestamp.second == 0:
        new_data = {
            'Symbol': bar.S,
            'Timestamp': bar.t,
            'Open': bar.o,
            'High': bar.h,
            'Low': bar.l,
            'Close': bar.c,
            'Volume': bar.v
        }
        df = df.append(new_data, ignore_index=True)

# Initialize Stream
stream = Stream(API_KEY,
                API_SECRET,
                base_url=URL(BASE_URL),
                data_feed='iex')

# Subscribe to bar updates for TSLA using the asynchronous bar handler
stream.subscribe_bars(bar_handler, 'TSLA')

def run_stream():
    stream.run()

def stop_stream():
    stream.close()
    # Save the DataFrame only if it's not empty
    if not df.empty:
        df.to_csv('hourly_bars.csv', mode='a', header=not pd.read_csv('hourly_bars.csv').shape[0], index=False)
        print("Data saved and stream stopped.")
    df.drop(df.index, inplace=True)  # Clear the DataFrame after saving

def schedule_stream():
    threading.Thread(target=run_stream).start()

# Schedule the stream to start every hour at 55 minutes past the hour
schedule.every().hour.at(":58").do(schedule_stream)

# Schedule the stream to stop 10 minutes later
schedule.every().hour.at(":02").do(stop_stream)

while True:
    schedule.run_pending()
    time.sleep(1)
