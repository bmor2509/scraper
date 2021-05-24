#Imports
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time

# Initialising CoinGecko API 
cg=CoinGeckoAPI()
 
# An array that holds the names of all coins that are going to be checked
gecko_list=['bitcoin', 'ethereum', 'ripple']

# An empty object that will be populated with data from the for loop
data = {}

# A for loop that iterates through the coin list and identifies changes in price over short intervals that could indicate a bullish or bearish trend
for coin in gecko_list:
    try:
        
        #Current prices
        current_coin_value = cg.get_price(ids=coin, vs_currencies='usd')
        current_prices = current_coin_value[coin]
        currency = current_prices['usd']
        print(currency)

        #Historical prices
        history = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days='1')['prices']
        data[coin]={}
        data[coin]['timestamps'], data[coin]['values']=zip(*history)
    except Exception as e:
        print(e)
        print('coin: ' + coin)
    
    if 
 
 # Constructs a pandas dataframe based on the coin data that is returned 
frame_list = [
    pd.DataFrame(data[coin]['values'], index=data[coin]['timestamps'], columns=[coin])
    for coin in gecko_list
    if coin in data
]
 
# print(frame_list)
 
 
#Write code to only add items to the dataframe when its value is not null / NaN
 
# Orders the dataframe
df_cryptocurrency = pd.concat(frame_list, axis=1).sort_index()
 
# Makes the dataframe more readable by partitioning the data with headers for each respective piece of information from a coin
df_cryptocurrency['datetime'] = pd.to_datetime(df_cryptocurrency.index, unit='ms')
df_cryptocurrency['date'] = df_cryptocurrency['datetime'].dt.date 
df_cryptocurrency['hour'] = df_cryptocurrency['datetime'].dt.hour
 
# Reformats the Dataframe from a wide to a long format 
df_cryptocurrency = df_cryptocurrency.melt(
    id_vars=["datetime", "date", "hour"], var_name="currency_name", ignore_index=True
)
 
# Sets display options for the dataframe to not limit how many results are shown
pd.set_option("display.max_rows", None, "display.max_columns", None)
 
# Removes any "Null" results from the dataframe 
cleaned_df = df_cryptocurrency.dropna()
# print(cleaned_df.head(5))
 
print(cleaned_df)


prev_price_history = {'currency_name': 'bitcoin'}
for index, price_history in cleaned_df.iterrows():
    if price_history['currency_name'] == prev_price_history['currency_name']:
        prev_price_history = price_history
    else:
        print('Last price history for ', prev_price_history['currency_name'], ' is ', prev_price_history['value'])
        prev_price_history = price_history
print('Last price history for', prev_price_history['currency_name'], ' is ', prev_price_history['value'])