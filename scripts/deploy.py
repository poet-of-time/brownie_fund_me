from brownie import FundMe, MockV3Aggregator, config, network
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me(): 
    # account = accounts.add(config["wallets"]["from_key"])
    account = get_account()
    # pass the price feed address to our fundme contract
    #if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print("lets deploy a mock")
        print(MockV3Aggregator)
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # publish_source = True is used to verify the contract on etherscan and get the 
    # green checkmark next to the contract
    # this along with ETHERSCAN_TOKEN in .env the token is an api key that can
    # be grabbed in your profile on etherscan.
    fund_me = FundMe.deploy(
        #we need to pass in an address to the FundMe.sol constructor. that is what the price_feed_address is
        price_feed_address, 
        {'from':account}, 
        publish_source = config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed at {fund_me.address}")
    # need the return when running tests
    return fund_me

def main():
    deploy_fund_me()