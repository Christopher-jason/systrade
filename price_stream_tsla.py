import pandas as pd
import config
from alpaca_trade_api import Stream
from alpaca_trade_api.common import URL
import asyncio

API_KEY = config.API_KEY
API_SECRET = config.SECRET_KEY
BASE_URL = 'wss://stream.data.alpaca.markets/v2/iex'  # Adjust as needed (iex or sip)

# Initialize the DataFrame
df = pd.read_csv('tsla_live_prices.csv')

# Path to save the CSV file
csv_file_path = 'tsla_live_prices.csv'

# Function to handle trade updates
# Continue from where the function to handle trade updates is defined
async def trade_update_handler(t):
    global df
    # Check if the symbol is TSLA
    if t.symbol == 'TSLA':
        # Extract price and timestamp
        new_data = pd.DataFrame({
            'symbol': [t.symbol],
            'price': [t.price],
            'timestamp': [t.timestamp]
        })
        # Append to the DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        # Append the latest data to the CSV file
        df.tail(1).to_csv(csv_file_path, mode='a', header=not pd.read_csv(csv_file_path).shape[0], index=False)
        print(df.tail(1))  # Print the latest data entry

# Initialize the stream
stream = Stream(API_KEY, API_SECRET, base_url=URL(BASE_URL), data_feed='iex')  # use data_feed as per your subscription

# Subscribe to TSLA trades
stream.subscribe_trades(trade_update_handler, 'TSLA')

# Start the stream
def start_stream():
    try:
        stream.run()
    except KeyboardInterrupt:
        print("Stream stopped manually")
    finally:
        stream.stop()

# Run the stream in an asyncio loop to handle asynchronous functions
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_stream())

