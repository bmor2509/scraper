#Imports
from pycoingecko import CoinGeckoAPI
from datetime import *; from dateutil.relativedelta import *
import pandas as pd
import time
 
#Initialising the CoinGecko API
cg = CoinGeckoAPI()
 
 
#Gets market information for the top 100 coins on coinGecko, and displays their name and market cap in a pandas dataframe
markets = cg.get_coins_markets(vs_currency='usd', per_page=150)
pd.set_option('display.max_rows', 2000)
df_markets = pd.DataFrame(markets, columns=['id', 'market_cap'])
# print(df_markets)
 
 
#Takes the names of the top 100 coins on coinGecko and puts them in an array
name_array = df_markets['id'].to_numpy()
# print(name_array)
 
TODAY = date.today()
 
#Yesterdays date
yesterday = date.today()-timedelta(days=1)
#Last Sunday's date
previousday = TODAY+relativedelta(weekday=SU(-1))
# date.today()-timedelta(days=3)
 
 
#Stringified versions of two days ago date for formatting
day = yesterday.strftime("%d")
month = yesterday.strftime("%m")
year = yesterday.strftime("%Y")
weekday = yesterday.strftime("%A")
 
 
 
#Stringified versions of day 3 days ago
previous_day = previousday.strftime("%d")
previous_month = previousday.strftime("%m")
previous_year = previousday.strftime("%Y")
 
#Yesterdays date formatted for CoinGecko API
dateString = (day +"-"+ month+"-"+year)
 
#The day before yesterdays date formatted for CoinGecko API
previous_datestring = (previous_day +"-"+ previous_month+"-"+previous_year)
 
#A list of all the ID's that will be passed to the "get" request
idList = df_markets['id'].to_numpy()[:126]
 
# A for loop to iterate through the list of ID's and get historical data on them, then filters their "community data"
 
for i in idList:
    try:
 
        # A 1.3 second delay applied between each iteration to prevent API rate limits being reached
        time.sleep(1.3)

        # A variable that stores up to date information on each respective coin
        yesterday_social = cg.get_coin_by_id(id=i, localization = "false", tickers="false", market_data="false", developer_data="false")
        # A variable that stores historical information on each respective coin 
        previousday_social = cg.get_coin_history_by_id(id=i, date=previous_datestring)
 
        # Sentiment information for current/up to date data. 
        sentiment = yesterday_social['sentiment_votes_up_percentage']
        # Variable that stores the name of the coins
        coinName = yesterday_social['name']
       
        # Community data and twitter followers for current/up to date data
        followers = yesterday_social['community_data']
        twitter_followers_today = followers['twitter_followers'] 
    
        # Community data and twitter followers for last data update
        previous_followers = previousday_social['community_data']
        previous_twitter_followers=previous_followers['twitter_followers']
 
        # Updates the positive/negative sentiment for each respective coin depending on their score out of 100
        if(sentiment)>50:
            print(coinName + " has a majoritively positive sentiment")
        else:
            print(coinName + " has a majoritively negative sentiment")

        # Outputs the current number of twitter followers
        print(coinName + " current twitter followers:")
        print(twitter_followers_today)
 
        # Outputs the previous number of twitter followers as of the last API update
        print (coinName + " Twitter followers as of last update:")
        print(previous_twitter_followers) 
    except Exception as e:
        print(e)
 
# Prints alerts where twitter followers for a coin's respective twitter page followers have risen by more than 20% in any 24 hour period
# If follower data isn't available or is null for any reason, the console prints "incomplete data"
    if (followers['twitter_followers']) is not None and (previous_followers['twitter_followers']):
        if (followers['twitter_followers']/previous_followers['twitter_followers']*100)>120:
            print(coinName+" Is up by more than 20 percent in Twitter followers over a 24 hour period, buy this coin ...")
        else:
            print("incomplete data or no significant rise")