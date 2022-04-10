from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network, accounts, exceptions
import pytest


# format for individual testing
# > brownie test -k test_only_owner_can_withdraw --network rinkey (if you're choosing a specific network to run test on)

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

# checks to make sure that if not owner tries to withdraw, contract will prevent from happening
def test_only_owner_can_withdraw():
    # running test on a test/main net is time consuming, so if you don't want to run this test
    # when testing on a test/main net, just add the pytest.skip if network is no local eg. ganache, hardhat,
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # from, is the address at which the contract was deployed from, meaning the owner of the contract
    # running this should throw error summary:
    # FAILED tests/test_fund_me.py::test_only_owner_can_withdraw - brownie.exceptions.VirtualMachineError: revert
    # this is what we want to occur
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})