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
    # you don't need to deploy a new mock if there is always a mock that is deployed
    # so this will only deploy if there hasn't always been a mock deployed, hence the <= 0
    # deploying mocks is something that is done pretty frequently so you can make it a function
    print(len(MockV3Aggregator))
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from":get_account()})
    print("Mocks Deployed!")