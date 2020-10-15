#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### Optional

## 2. Explore CryptoControl data API


# In[4]:


from crypto_news_api import CryptoControlAPI
import pandas as pd
import json

# import api key
with open('CryptoControl_api_key.json', mode='r') as key_file:
    cc_key = json.loads(key_file.read())['key']


# In[5]:


# Connect to the CryptoControl API
cc_api = CryptoControlAPI(cc_key)


# In[6]:


# Get top news, display with Dataframe
pd.DataFrame(cc_api.getTopNews())


# In[7]:


# get latest Chinese news
latest_cn = cc_api.getLatestNews("cn")
pd.DataFrame(latest_cn)


# In[8]:


# get top bitcoin news
top_bitcoin = cc_api.getTopNewsByCoin("bitcoin")
pd.DataFrame(top_bitcoin)


# In[10]:


# Get news articles grouped by category.
top_cat = cc_api.getTopNewsByCategory('cn')
pd.DataFrame(top_cat['analysis'])


# In[11]:


# get top EOS tweets
EOS_tweets = cc_api.getTopTweetsByCoin("eos")
pd.DataFrame(EOS_tweets)


# In[12]:


# get top bitcoin reddit posts
bitcoin_reddit = cc_api.getLatestRedditPostsByCoin("bitcoin")
pd.DataFrame(bitcoin_reddit)


# In[13]:


# get reddit/tweets/articles in a single combined feed for NEO
neo_top_feed = cc_api.getTopFeedByCoin("neo")
pd.DataFrame(neo_top_feed)


# In[14]:


# Get reddit/tweets/articles (seperated) for a particular coin (sorted by time)
eos_news=cc_api.getTopItemsByCoin("eos", "jp")
pd.DataFrame(eos_news)


# In[15]:


# get latest reddit/tweets/articles (seperated) for Litecoin
Latest_litecoin=cc_api.getLatestItemsByCoin("litecoin")
pd.DataFrame(Latest_litecoin)


# In[16]:


# get details (subreddits, twitter handles, description, links) for ethereum
detail=cc_api.getCoinDetails("ethereum")
pd.DataFrame(detail['links'])


# In[ ]:




