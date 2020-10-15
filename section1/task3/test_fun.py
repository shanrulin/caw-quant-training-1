### Optional

#### 1. learn Unittest in python

## use pytest
from etherscan.accounts import Account
import json

with open('C:/Users/USER/Desktop/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

address = '0x2a65aca4d5fc5b5c859090a6c34d164135398226'
page = 1
offset = 2

def test_get_balance():
    api = Account(address=address, api_key=key)
    assert api.get_balance() == '2517932069507380044250'

def test_get_transaction_page():
    api = Account(address=address, api_key=key)
    assert api.get_transaction_page(page, offset)[1]['gas'] == '90000' 
