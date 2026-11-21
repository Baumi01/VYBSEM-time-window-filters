import json
from web3 import Web3

# connect to the local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
RA = w3.eth.accounts[0]                         # registration authority, first account


# deploys contract on the blockchain and returns it
def deploy(name):
    path = f"chain/artifacts/contracts/{name}.sol/{name}.json"
    
    # load compiled contract
    with open(path) as f:
        compiled = json.load(f)

    abi = compiled["abi"]               # list of contract functions (insert, remove)
    bytecode = compiled["bytecode"]     # compiled code to be saved on a blockchain

    # send a transaction, which will create contract on the blockchain
    blueprint = w3.eth.contract(abi=abi, bytecode=bytecode)     # plan of a contract (class in python)
    tx_hash = blueprint.constructor().transact({"from": RA})    # creates a contract on a blockchain

    # wait until the transaction is recorded on the blockchain
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)      # keeps the address of a contract with used gas
    address = receipt.contractAddress                           # address where contract is on the blockchain

    # return object, from which contract functions will be called
    return w3.eth.contract(address=address, abi=abi)


# send a transaction to the blockchain and returns how much gas it cost
def send(function_call):
    # send a transaction from RA account
    tx_hash = function_call.transact({"from": RA})

    # wait until the transaction is recorded on the blockchain
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)      # confirmation of the transaction (contains used gas)

    # return used gas
    return receipt.gasUsed


# creates pseudonym of a device for current time window
def pseudonym(device, window):
    # connect device number and window number into text
    text = f"{device}-{window}"

    # hash the text to unique 32 byte value
    return Web3.keccak(text=text)



def test():
    original = deploy("OriginalFilter")
    windows = deploy("WindowFilter")
    p = pseudonym(7, 5)

    gas = send(original.functions.insert(p))
    print("Original insert gas:", gas)
    print("Original isRevoked:", original.functions.isRevoked(p).call())   # True

    gas = send(original.functions.remove(p))
    print("Original remove gas:", gas)
    print("Original isRevoked:", original.functions.isRevoked(p).call())   # False

    gas = send(windows.functions.insert(5, p))
    print("Window insert gas:", gas)
    print("Window isRevoked:", windows.functions.isRevoked(5, p).call())   # True

    gas = send(windows.functions.discardWindow(5))
    print("Window discard gas:", gas)
    print("Window isRevoked:", windows.functions.isRevoked(5, p).call())   # False

test()