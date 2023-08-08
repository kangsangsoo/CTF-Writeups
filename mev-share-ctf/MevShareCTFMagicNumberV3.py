

from secret import private_key
from web3 import Web3, Account
import requests
from eth_account.messages import encode_defunct
import json
from solcx import compile_source, install_solc
import threading

# rpc_url = "https://goerli.infura.io/v3/9e312d162fe54da08aab66c68e491831"
rpc_url = "https://ethereum-goerli.publicnode.com"
sse_url = "https://mev-share-goerli.flashbots.net/"
relay_url = "https://relay-goerli.flashbots.net/"

w3 = Web3(Web3.HTTPProvider(rpc_url))


# install_solc("0.8.19")

# sources = open("Checker.sol", "r").read()
# compiled_sol = compile_source(sources, output_values=['abi', 'bin'])


# abi, bin = compiled_sol["<stdin>:Checker"]['abi'], compiled_sol["<stdin>:Checker"]['bin']

# print(abi)
# print(bin)

# my_account = w3.eth.account.from_key(private_key)

# checker = w3.eth.contract(abi=abi, bytecode=bin)
# transaction = checker.constructor().build_transaction({
#     "chainId": w3.eth.chain_id,
#     "gasPrice": w3.eth.gas_price,
#     "from": my_account.address,
#     "nonce": w3.eth.get_transaction_count(my_account.address),
# })


# tx_hash = w3.eth.send_raw_transaction(my_account.sign_transaction(transaction).rawTransaction)
# rec = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(rec)

# checker_addr = rec.contractAddress
# print(checker_addr) 

checker_addr = "0xbE0d1B1990Cec561c6d9e178C51148E268EA97aD"
# checker = w3.eth.contract(address=checker_addr, abi=abi)


# def event_stream(url):
#     while True:
#         event = []
#         try:
#             with requests.get(url, stream=True, timeout=4) as response:
            
#                 for line in response.iter_lines():
#                     if line:  # filter out keep-alive new lines
#                         event.append(line)
#         except:
#                 yield event

def event_stream(url):
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield line


def send_bundle(hash, block_number, magic_number, nonce, to):
    data = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "mev_sendBundle",
        "params": [
            {
                "version": "v0.1",
                "inclusion": {
                    "block": hex(block_number),
                    "maxBlock": hex(block_number+20),
                },
                "body": [
                    {'hash': hash},
                ],
            }
        ],
    }
    data['params'][0]['body'].append({
        "tx": Account.sign_transaction(
            {
                "gas": 10 ** 12,
                "maxFeePerGas": 2 * 10 ** 13,
                "maxPriorityFeePerGas": 2 * 10 ** 13,
                "data": "0xae169a50" + hex(magic_number)[2:].rjust(64, '0'), 
                "nonce": nonce,
                "to": to, 
                "value": "0x0", 
                "chainId": 5,
            }, 
            private_key
        ).rawTransaction.hex(),
        "canRevert": False,
    })
    data['params'][0]['body'].append({
        "tx": Account.sign_transaction(
            {
                "gas": 10 ** 12,
                "maxFeePerGas": 2 * 10 ** 13,
                "maxPriorityFeePerGas": 2 * 10 ** 13,
                "data": "0xcf5303cf", 
                "nonce": nonce + 1,
                "to": checker_addr, 
                "value": "0x0", 
                "chainId": 5,
            }, 
            private_key
        ).rawTransaction.hex(),
        "canRevert": False,
    })
    # print(data)
    message = encode_defunct(text=Web3.keccak(text=json.dumps(data)).hex())
    headers = {
        "Content-Type": "application/json",
        "X-Flashbots-Signature": Account.from_key(private_key).address + ":" +  Account.sign_message(message, private_key).signature.hex(),
    }
    print(requests.post(url=relay_url, data=json.dumps(data), headers=headers).content)


ADDR = Web3.to_checksum_address(0xE8B7475e2790409715AF793F799f3Cc80De6f071)

for events in event_stream(sse_url):
    try:
        data = json.loads(events[5:])
    except:
        continue
    print("==================")


    if data['logs']:
        if 'topics' in data['logs'][0]:
            if data['logs'][0]['topics'][0] == "0x86a27c2047f889fafe51029e28e24f466422abe8a82c0c27de4683dda79a0b5d":
                if Web3.to_checksum_address(data['logs'][0]['address']) == ADDR:
                        

                    lower_bound = int(data['logs'][0]['data'][2:66], 16)
                    upper_bound = int(data['logs'][0]['data'][66:], 16)

                    bn = w3.eth.get_block_number()
                    nn = w3.eth.get_transaction_count(Account.from_key(private_key).address)

                    print("find ", str(bn), str(data['hash']))

                    # ths = []
                    for mn in range(lower_bound, upper_bound+1):
                        # t = threading.Thread(target=send_bundle,args=(data['hash'], bn, mn, nn, ADDR))
                        send_bundle(data['hash'], bn, mn, nn, ADDR)
                        # t.start()
                        # ths.append(t)

                    # for th in ths:
                    #     th.join()
                            





