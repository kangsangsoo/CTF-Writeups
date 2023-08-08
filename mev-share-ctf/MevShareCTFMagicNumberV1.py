

from secret import private_key
from web3 import Web3, Account
import requests
from eth_account.messages import encode_defunct
import json
from solcx import compile_source, install_solc
import threading

rpc_url = "https://ethereum-goerli.publicnode.com"
sse_url = "https://mev-share-goerli.flashbots.net/"
relay_url = "https://relay-goerli.flashbots.net/"

w3 = Web3(Web3.HTTPProvider(rpc_url))

def event_stream(url):
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield line


for events in event_stream(sse_url):
    try:
        data = json.loads(events[5:])
    except:
        continue
    print("==================")


    if data['logs']:
        if 'topics' in data['logs'][0]:
            if data['logs'][0]['topics'][0] == "0x86a27c2047f889fafe51029e28e24f466422abe8a82c0c27de4683dda79a0b5d":
                
                    
                lower_bound = int(data['logs'][0]['data'][2:66], 16)
                upper_bound = int(data['logs'][0]['data'][66:], 16)

                block_number = w3.eth.get_block_number()

                data_to_be_sent = {
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
                                {'hash': data['hash']},
                            ],
                        }
                    ],
                }

                nn = 0
                for idx in range(lower_bound, upper_bound+1):
                    data_to_be_sent['params'][0]['body'].append({
                        "tx": Account.sign_transaction({
                            "gas": 10 ** 12,
                            "maxFeePerGas": 2 * 10 ** 13,
                            "maxPriorityFeePerGas": 2 * 10 ** 13,
                            "data": "0xae169a50" + hex(idx)[2:].rjust(64, '0'), 
                            "nonce": w3.eth.get_transaction_count(Account.from_key(private_key).address) + nn,
                            "to": Web3.to_checksum_address(data['logs'][0]['address']), 
                            "value": "0x0", 
                            "chainId": 5,
                            }, 
                            private_key
                        ).rawTransaction.hex(),
                        "canRevert": True,
                        }
                    )
                    nn += 1

                message = encode_defunct(text=Web3.keccak(text=json.dumps(data_to_be_sent)).hex())
                headers = {
                    "Content-Type": "application/json",
                    "X-Flashbots-Signature": Account.from_key(private_key).address + ":" +  Account.sign_message(message, private_key).signature.hex(),
                }
                print(requests.post(url=relay_url, data=json.dumps(data_to_be_sent), headers=headers).content)



