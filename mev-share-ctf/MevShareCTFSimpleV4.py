import json
import requests
from web3 import Web3, Account
from web3 import EthereumTesterProvider
from eth_account.messages import encode_defunct

from secret import private_key

rpc_url = "https://ethereum-goerli.publicnode.com/"
sse_url = "https://mev-share-goerli.flashbots.net/"
relay_url = "https://relay-goerli.flashbots.net/"

w3 = Web3(Web3.HTTPProvider(rpc_url))

def event_stream(url):
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield line

for event in event_stream(sse_url):
    try:
        data = json.loads(event[5:])
    except:
        continue
    

    print("=======")

    
    if True:
        if True:

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
                    "data": "0xb88a80df", 
                    "nonce": w3.eth.get_transaction_count(Account.from_key(private_key).address),
                    "to": Web3.to_checksum_address("0x20a1A5857fDff817aa1BD8097027a841D4969AA5"), 
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