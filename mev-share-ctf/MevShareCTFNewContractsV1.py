

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
            if data['logs'][0]['topics'][0] == "0xf7e9fe69e1d05372bc855b295bc4c34a1a0a5882164dd2b26df30a26c1c8ba15":
                
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

                data_to_be_sent['params'][0]['body'].append({
                    "tx": Account.sign_transaction({
                        "gas": 10 ** 12,
                        "maxFeePerGas": 2 * 10 ** 13,
                        "maxPriorityFeePerGas": 2 * 10 ** 13,
                        "data": "0xb88a802f",
                        "nonce": w3.eth.get_transaction_count(Account.from_key(private_key).address),
                        "to": Web3.to_checksum_address(data['logs'][0]['data'][-40:]), 
                        "value": "0x0", 
                        "chainId": 5,
                        }, 
                        private_key
                    ).rawTransaction.hex(),
                    "canRevert": False,
                    }
                )

                message = encode_defunct(text=Web3.keccak(text=json.dumps(data_to_be_sent)).hex())
                headers = {
                    "Content-Type": "application/json",
                    "X-Flashbots-Signature": Account.from_key(private_key).address + ":" +  Account.sign_message(message, private_key).signature.hex(),
                }
                print(requests.post(url=relay_url, data=json.dumps(data_to_be_sent), headers=headers).content)



