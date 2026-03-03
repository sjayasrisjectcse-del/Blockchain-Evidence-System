from web3 import Web3
from config import RPC_URL, CONTRACT_ADDRESS
from contract_abi import ABI

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
account = w3.eth.accounts[0]

def store_evidence(file_hash, file_name):
    tx = contract.functions.storeEvidence(file_hash, file_name).transact({
        "from": account
    })
    return tx.hex()

def get_evidence(index):
    return contract.functions.getEvidence(index).call()

def get_count():
    return contract.functions.getCount().call()