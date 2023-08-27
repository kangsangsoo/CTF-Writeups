# sample solve script to interface with the server
import pwn

# feel free to change this
account_metas = [
    ("program", "-r"),  # read only
    ("data account", "-w"), # writable
    ("user", "sw"), # signer + writable
    ("user data", "sw"),
    ("mp", "-"),
    ("system program", "-"),
]

from Crypto.Util.number import *
instruction_data = "placeholder"

p = pwn.remote("chals.sekai.team",  5043)

with open("solve/target/deploy/solve.so", "rb") as f:
    solve = f.read()

p.sendlineafter(b"program pubkey: \n", b"My11111111111111111111111111111111111111112")
p.sendlineafter(b"program len: \n", str(len(solve)).encode())
p.send(solve)

accounts = {}
for l in p.recvuntil(b"num accounts: \n", drop=True).strip().split(b"\n"):
    [name, pubkey] = l.decode().split(": ")
    accounts[name] = pubkey

accounts['mp'] = "My11111111111111111111111111111111111111112"
accounts['system program'] = "11111111111111111111111111111111"

p.sendline(str(len(account_metas)).encode())
for (name, perms) in account_metas:
    p.sendline(f"{perms} {accounts[name]}".encode())
p.sendlineafter(b"ix len: \n", str(len(instruction_data)).encode())
p.send(instruction_data)

p.interactive()
