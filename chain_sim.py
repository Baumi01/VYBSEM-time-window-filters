import json
from web3 import Web3
from simulation import generate_scenario

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


# runs the original design (Cui et al.) - one filter, per-entry deletion
def run_original(revoked):
    contract = deploy("OriginalFilter")
    tx_count = 0
    gas_total = 0

    for device, window, k in revoked:
        for j in range(window, window + k):
            p = pseudonym(device, j)

            gas_total += send(contract.functions.insert(p))
            tx_count += 1

            gas_total += send(contract.functions.remove(p))
            tx_count += 1

    return tx_count, gas_total


# runs the proposed design - one filter per time window, discarded as a whole
def run_windows(revoked):
    contract = deploy("WindowFilter")
    tx_count = 0
    gas_total = 0
    used_windows = []

    for device, window, k in revoked:
        for j in range(window, window + k):
            p = pseudonym(device, j)

            gas_total += send(contract.functions.insert(j, p))
            tx_count += 1

            if j not in used_windows:
                used_windows.append(j)

    for i in used_windows:
        gas_total += send(contract.functions.discardWindow(i))
        tx_count += 1

    return tx_count, gas_total


# runs both designs 
def run_on_chain(revoked):
    original_tx, original_gas = run_original(revoked)
    window_tx, window_gas = run_windows(revoked)

    return original_tx, original_gas, window_tx, window_gas


if __name__ == "__main__":
    revoked = generate_scenario(1000, 100, 10, 0.05, seed=1)

    original_tx, original_gas, window_tx, window_gas = run_on_chain(revoked)

    print("Revoked devices:", len(revoked))
    print(f"Original: {original_tx} transactions, {original_gas} gas")
    print(f"Windows: {window_tx} transactions, {window_gas} gas")
    print(f"Saved transactions: {(original_tx - window_tx) / original_tx * 100:.1f}%")
    print(f"Saved gas:          {(original_gas - window_gas) / original_gas * 100:.1f}%")