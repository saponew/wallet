# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv

# Import constants.py and necessary functions from bit and web3
from constants import *
from web3 import Web3
from decimal import Decimal
from eth_account import Account
from bit import wif_to_key, PrivateKeyTestnet, network
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middle_ware, layer = 0)

# Load and set environment variables
load_dotenv("api.env")
mnemonic = os.getenv("mnemonic")

# Create a function called `derive_wallets`
def derive_wallets(coin = BTC, mnemonic = mnemonic, depth = 3):
    command = f"./derive -g --mnemonic = '{mnenmonic}' --coin = {coin} --numderive = {depth} --format = json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {'ETH': derive_wallets(coin = ETH), 
        'BTCTEST': derive_wallets(coin = BTCTEST),
        'BTC': derive_wallets(coin = BTC)}


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST: 
        return PrivateKeyTestnet(priv_key)


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, ):
    if coin == BTCTEST:
        return account.prepare_transaction(account.address, [(recipient, amount, BTC)])
    else:
        amount = w3.toWei(Decimal(amount), 'ether')
        gasEstimate: w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address, 
            "to": to, 
            "value": amount,
            "gasPrice": w3.eth.gasPrice, 
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": 
        }
    
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH, 5)[0]['privkey'])
    
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    
    
    if coin == ETH:
        txn_eth = create_tx(coin, account, recipient, amount)
        signed_txn_eth = account.sign_transaction(txn_eth)
        result = w3.eth.sendRawTransaction(signed_txn_eth.rawTransaction)
        print(result.hex())
        return result.hex()
    
    else coin == BTCTEST:
        
        txn_btctest = create_tx(coin, account, recipient, amount)
        signed_txn_btctest = account.sign_transaction(txn_btctest)
        return NetworkAPI.broadcast_tx_testnet(signed_txn_btctest)
        return signed_txn_btctest
    