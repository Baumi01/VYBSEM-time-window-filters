from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

print("Connection:", w3.is_connected())
print("Number of last block:", w3.eth.block_number)
print("First account:", w3.eth.accounts[0])