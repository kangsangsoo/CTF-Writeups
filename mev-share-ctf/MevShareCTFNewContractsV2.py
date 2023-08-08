

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
            if data['logs'][0]['topics'][0] == "0x71fd33d3d871c60dc3d6ecf7c8e5bb086aeb6491528cce181c289a411582ff1c":

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


                
                from web3.utils.address import get_create2_address

                addr = get_create2_address("0x5eA0feA0164E5AA58f407dEBb344876b5ee10DEA", data['logs'][0]['data'], "60a060405233608052436000556080516101166100266000396000606f01526101166000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806396b81609146037578063b88a802f146051575b600080fd5b603f60005481565b60405190815260200160405180910390f35b60576059565b005b4360005414606657600080fd5b600080819055507f00000000000000000000000000000000000000000000000000000000000000006001600160a01b031663720ecf456040518163ffffffff1660e01b8152600401600060405180830381600087803b15801560c757600080fd5b505af115801560da573d6000803e3d6000fd5b5050505056fea26469706673582212207a00db890eff47285ac0d9c9b8735727d476952aa87b45ee82fd6bb4f42c6fa764736f6c63430008130033")

                data_to_be_sent['params'][0]['body'].append({
                    "tx": Account.sign_transaction({
                        "gas": 10 ** 12,
                        "maxFeePerGas": 2 * 10 ** 13,
                        "maxPriorityFeePerGas": 2 * 10 ** 13,
                        "data": "0xb88a802f",
                        "nonce": w3.eth.get_transaction_count(Account.from_key(private_key).address),
                        "to": Web3.to_checksum_address(addr), 
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



