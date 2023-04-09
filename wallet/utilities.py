from eth_account import Account
from web3 import Web3
from eth_keys import keys


def create_eth_account():
    acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    address = acct.address
    private_key = acct.key
    public_key = keys.PrivateKey(private_key).public_key
    # print(f"Address: {address}")
    # print(f"Private key: {private_key.hex()}")
    # print(f"Public key: {public_key}")
    return [private_key, public_key]


def get_current_balance(address):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-INFURA-PROJECT-ID'))
    addr = address

    balance = w3.eth.get_balance(addr)
    balance_ether = w3.fromWei(balance, 'ether')

    print(f"Address: {address}")
    print(f"Balance: {balance} wei")
    print(f"Balance: {balance_ether} ether")

