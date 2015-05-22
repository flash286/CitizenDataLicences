from ethereum.slogging import configure_logging
from ethereum.utils import to_string
from ethereum import abi

__author__ = 'nikolas'
from ethereum import transactions, blocks, utils, processblock, slogging
from ethereum.db import DB as EthDB
import serpent

configure_logging(':trace')

key = utils.sha3("key")
key2 = utils.sha3("key2")

addr = utils.privtoaddr(key)
addr2 = utils.privtoaddr(key2)

print addr, addr2

db = EthDB()

genesis = blocks.genesis(db=db, start_alloc={addr: {"wei": to_string(2 ** 200)}})

print genesis.account_to_dict(address=addr)

tx = transactions.Transaction(0, 21000, 21000, addr2, 56789000, "").sign(key)

success, _ = processblock.apply_transaction(genesis, tx=tx)

print genesis.account_to_dict(addr)
print genesis.account_to_dict(addr2)


serpent_code = open("namecoin.se").read()
serpent.compile_to_lll(serpent_code)
serpent.pretty_compile(serpent_code)
bytecode = serpent.compile(serpent_code)

print bytecode

tx2 = transactions.contract(genesis.get_nonce(addr), 21000, 21000 * 100, 0, bytecode).sign(key)
success, contract_addr = processblock.apply_transaction(genesis, tx2)

print  genesis.account_to_dict(contract_addr)

msg = transactions.Transaction(genesis.get_nonce(addr), 1000, 10000, contract_addr, 0, serpent.encode_abi())
