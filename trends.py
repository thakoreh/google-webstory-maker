#import the libraries
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()
# Get realtime Google Trends data
# df = pytrend.trending_searches(pn='united_states')
# df.head()


df = pytrend.trending_searches(pn='united_states')
df.head()

df = pytrend.realtime_trending_searches(pn='US')


df.head()


# https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all