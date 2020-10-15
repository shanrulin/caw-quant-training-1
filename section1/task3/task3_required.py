#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### Required

#### 1. **Use Etherscan Python SDK** to get on-chain data


# ### - [ ] play and combine scripts in examples/accounts

# In[1]:


from etherscan.accounts import Account
import json


#address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a
#0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b

# import api key
with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']


# Setup api for single address
address = '0x2a65aca4d5fc5b5c859090a6c34d164135398226'
api = Account(address=address, api_key=key)


# In[2]:


## get balance
api.get_balance()


# In[26]:


trans_page = api.get_transaction_page(page=1, offset=2)


# In[49]:


trans_page


# In[27]:


import pandas as pd
df_trans_page = pd.DataFrame(trans_page)
df_trans_page


# In[28]:


blocks_minded = api.get_blocks_mined_page(page=1, offset=10, blocktype='blocks')
pd.DataFrame(blocks_minded)


# In[5]:


#help('etherscan')

#PACKAGE CONTENTS
#    accounts
#    client
#    contracts
#    errors
#    etherscan
#    proxies
#    stats
#    tokens


# ### - [ ] play and combine scripts in examples/blocks

# In[6]:


### No module named 'etherscan.blocks'...
#from etherscan.blocks import Blocks

#block = 9551218
#api_block = Blocks(api_key=key)

# Get the block reward
#reward = api_block.get_block_reward(block)
#reward


# ### - [ ] play and combine scripts in examples/contracts

# In[30]:


from etherscan.contracts import Contract

address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'

api_contract = Contract(address=address, api_key=key)
abi = api_contract.get_abi()
print(abi)


# In[47]:


source_code = Contract(address=address, api_key=key)
print(source_code)


# ### - [ ] play and combine scripts in examples/proxies

# In[10]:


from etherscan.proxies import Proxies

api_proxies = Proxies(api_key=key)
block = api_proxies.get_block_by_number(9551218)
print(block['number'])


# In[34]:


tx_count = api_proxies.get_block_transaction_count_by_number(block_number='0x91bd72')
print(int(tx_count, 16))


# In[44]:


TX_HASH = '0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1'

transaction = api_proxies.get_transaction_by_hash(tx_hash=TX_HASH)

pd.DataFrame(transaction,index=[0])


# ### - [ ] play and combine scripts in examples/stats

# In[46]:


from etherscan.stats import Stats

api_stats = Stats(api_key=key)
last_price = api_stats.get_ether_last_price()
#print(last_price)
pd.DataFrame(last_price, index=[0])


# In[16]:


ether_supply = api_stats.get_total_ether_supply()
print(ether_supply)


# ### - [ ] play and combine scripts in examples/tokens

# In[20]:


from etherscan.tokens import Tokens

contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
address = "0xe04f27eb70e025b78871a2ad7eabe85e61212761"

api_token = Tokens(contract_address=contract_address, api_key=key)

# Get token balance of an address
api_token.get_token_balance(address)


# In[23]:


# Get total supply of tokens
api_token.get_total_supply()


# ### - [ ] play and combine scripts in examples/transactions

# In[48]:


### No module named 'etherscan.transactions'...
#from etherscan.transactions import Transactions

#api_trans = Transactions(api_key=key)
#status = api_trans.get_status(tx_hash=TX_HASH)
#print(status)

#receipt_status = api_trans.get_tx_receipt_status(tx_hash=TX_HASH)
#print(receipt_status)

