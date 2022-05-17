from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print("You are currently running on a development chain")
        print(accounts[0])
        return accounts[0]
    else:
        print("You are currently running on a testnet")
        print(accounts.add(config["wallets"]["from_key"]))
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    print(len(MockV3Aggregator))
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from":get_account()})
    print("Mocks Deployed!")