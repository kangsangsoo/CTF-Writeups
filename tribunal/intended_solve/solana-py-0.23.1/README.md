<div align="center">
    <img src="https://raw.githubusercontent.com/michaelhly/solana-py/master/docs/img/solana-py-logo.jpeg" width="25%" height="25%">
</div>

---

[![Actions
Status](https://github.com/michaelhly/solanapy/workflows/CI/badge.svg)](https://github.com/michaelhly/solanapy/actions?query=workflow%3ACI)
[![PyPI version](https://badge.fury.io/py/solana.svg)](https://badge.fury.io/py/solana)
[![Codecov](https://codecov.io/gh/michaelhly/solana-py/branch/master/graph/badge.svg)](https://codecov.io/gh/michaelhly/solana-py/branch/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/michaelhly/solana-py/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Solana.py

**🐍 The Solana Python SDK 🐍**

Solana.py is the base Python library for interacting with Solana.
You can use it to build transactions and interact
with the
[Solana JSON RPC API](https://docs.solana.com/apps/jsonrpc-api),
much like you would do with
[solana-web3.js](https://github.com/solana-labs/solana-web3.js/)

It also covers the
[SPL Token Program](https://spl.solana.com/token).

[Latest Documentation](https://michaelhly.github.io/solana-py/).

**⚓︎ See also: [AnchorPy](https://github.com/kevinheavey/anchorpy),**
**a Python client for**
**[Anchor](https://project-serum.github.io/anchor/getting-started/introduction.html)-based**
**programs on Solana. ⚓︎**

## ⚡ Quickstart

### Installation

```sh
pip install solana
```

### General Usage

Note: check out the
[Solana Cookbook](https://solanacookbook.com/)
for more detailed examples!

```py
import solana
```

### API Client

```py
from solana.rpc.api import Client

http_client = Client("https://api.devnet.solana.com")
```

### Async API Client

```py
import asyncio
from solana.rpc.async_api import AsyncClient

async def main():
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
    print(res)  # True

    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True
    await client.close()

asyncio.run(main())
```

### Websockets Client

```py
import asyncio
from asyncstdlib import enumerate
from solana.rpc.websocket_api import connect

async def main():
    async with connect("ws://api.devnet.solana.com") as websocket:
        await websocket.logs_subscribe()
        first_resp = await websocket.recv()
        subscription_id = first_resp.result
        next_resp = await websocket.recv()
        print(next_resp)
        await websocket.logs_unsubscribe(subscription_id)

    # Alternatively, use the client as an infinite asynchronous iterator:
    async with connect("ws://api.devnet.solana.com") as websocket:
        await websocket.logs_subscribe()
        first_resp = await websocket.recv()
        subscription_id = first_resp.result
        async for idx, msg in enumerate(websocket):
            if idx == 3:
                break
            print(msg)
        await websocket.logs_unsubscribe(subscription_id)

asyncio.run(main())
```

## 🔨 Development

### Setup

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Install dev dependencies:

```sh
poetry install

```

3. Activate the poetry shell.

```sh
poetry shell
```

### Lint

```sh
make lint
```

### Tests

```sh
# All tests
make tests
# Unit tests only
make unit-tests
# Integration tests only
make int-tests
```
