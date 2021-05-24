#Imports
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
 
cg=CoinGeckoAPI()
 
 
#Gets market information for the top 100 coins on coinGecko, and displays their name and market cap in a pandas dataframe
markets = cg.get_coins_markets(vs_currency='usd', per_page=150)
pd.set_option('display.max_rows', 2000)
df_markets = pd.DataFrame(markets, columns=['id'])
# print(df_markets)
 
idList = df_markets['id'].to_numpy()[:10]
 
 
# A for loop that iterates through the list of coins and asseses their price fluctuations 
for x in idList:
    try:
        # A small delay between each iteration that prevents the API rate limits being reached 
        time.sleep(1.8)

        # A group of variables that can be used for accessing different sections of the coin data, ranging from a full set of data, to just the USD value
        currentPrices = cg.get_price(ids=x, vs_currencies='usd')
        current_price_value = currentPrices[x]
        currency = current_price_value['usd']

        # Fetches historical data for the previous day to compare against current values 
        prices = cg.get_coin_history_by_id(id = x, date='19-05-2021')
        
        # Variable that stores the name of each coin in turn
        coinName = prices['name']
 
        # A group of variables that can be used for accessing different sections of the historical coin data, ranging from a full set of data to just the USD value
        market = prices['market_data']
        current_price = market['current_price']
        USD = current_price['usd']

        # Prints the historical price, and then the current price
        print(USD)
        print(currency)
        
    except Exception as e:
        print(e)
 
    # An if statement that prints an alert when a coin has seen a price raise greater than 3 percent in a rolling 24 hour period
    if (currency/USD*100)>103:
        print(coinName +" has seen a price rise greater than 3 percent in the last 24 hours")
    else:
        print(coinName + " has not seen significant increase in the last 24 hours.")