import json

from ..jsonrpc.ethereumJSON import EthereumJSON


class EthereumAPI:
    def __init__(self):
        self.json = EthereumJSON()

    def coinbase(self):
        return self.json.sendJSONRequest("eth_coinbase")

    def set_coinbase(self, coinbase):
        return self.json.sendJSONRequest("eth_setCoinbase", coinbase)

    def send_transaction(self, from_addr, to_addr, gas, gasPrice, value, data):
        params = {
            "from": from_addr,
            "to": to_addr,
            "gas": gas,
            "gasPrice": gasPrice,
            "value": value,
            "data": data
        }
        return self.json.sendJSONRequest("eth_sendTransaction", params)

    def listening(self):
        return self.json.sendJSONRequest("eth_listening")

    def set_listening(self, listening):
        return self.json.sendJSONRequest("eth_setListening", listening)

    def mining(self):
        return self.json.sendJSONRequest("eth_mining")

    def set_mining(self, mining):
        return self.json.sendJSONRequest("eth_setMining", mining)

    def gas_price(self):
        return self.json.sendJSONRequest("eth_gasPrice")

    def accounts(self, client=None):
        return self.json.sendJSONRequest("eth_accounts", client)

    def peer_count(self):
        return self.json.sendJSONRequest("eth_peerCount")

    def default_block(self):
        return self.json.sendJSONRequest("eth_defaultBlock")

    def set_efault_block(self, block):
        return self.json.sendJSONRequest("eth_setDefaultBlock", block)

    def number(self):
        return self.json.sendJSONRequest("eth_number")

    def balance_at(self, address):
        return self.json.sendJSONRequest("eth_getBalance", address)

    def state_at(self, address, index):
        return self.json.sendJSONRequest("eth_stateAt", address, index)

    def storage_at(self, address):
        return self.json.sendJSONRequest("eth_storageAt", address)

    def count_at(self, address):
        return self.json.sendJSONRequest("eth_countAt", address)

    def transaction_count_by_Hash(self, hash):
        return self.json.sendJSONRequest("eth_transactionCountByHash", hash)

    def transaction_count_by_number(self, number):
        return self.json.sendJSONRequest("eth_transactionCountByNumber", number)

    def uncle_count_by_hash(self, hash):
        return self.json.sendJSONRequest("eth_uncleCountByHash", hash)

    def uncle_count_by_number(self, number):
        return self.json.sendJSONRequest("eth_uncleCountByNumber", number)

    def code_at(self, address):
        return self.json.sendJSONRequest("eth_codeAt", address)

    def transact(self, code):
        return self.json.sendJSONRequest("eth_transact", json.dumps({"code": code}))

    def call(self, params):
        return self.json.sendJSONRequest("eth_call", params, 'latest')

    def flush(self):
        return self.json.sendJSONRequest("eth_flush")

    def block_by_hash(self, hash):
        return self.json.sendJSONRequest("eth_blockByHash", hash)

    def block_by_number(self, number):
        return self.json.sendJSONRequest("eth_blockByNumber", number)

    def transaction_by_hash(self, hash, index):
        return self.json.sendJSONRequest("eth_transactionByHash", hash, index)

    def transaction_by_number(self, number, index):
        return self.json.sendJSONRequest("eth_transactionByNumber", number, index)

    def uncle_by_hash(self, hash, index):
        return self.json.sendJSONRequest("eth_uncleByHash", hash, index)

    def uncle_by_number(self, number, index):
        return self.json.sendJSONRequest("eth_uncleByNumber", number, index)

    def compilers(self):
        return self.json.sendJSONRequest("eth_compilers")

    def compile_solidity(self, contract):
        return self.json.sendJSONRequest("eth_compileSolidity", contract)

    def new_filter(self, topic):
        return self.json.sendJSONRequest("eth_newFilter", json.dumps({"topic": topic}))

    def new_filter_string(self, string):
        return self.json.sendJSONRequest("eth_newFilterString", string)

    def uninstall_filter(self, id):
        return self.json.sendJSONRequest("eth_uninstallFilter", id)

    def changed(self, id):
        return self.json.sendJSONRequest("eth_changed", id)

    def filter_logs(self, id):
        return self.json.sendJSONRequest("eth_filterLogs", id)

    def logs(self, topic):
        return self.json.sendJSONRequest("eth_logs", json.dumps({"topic": topic}))

    def get_work(self):
        return self.json.sendJSONRequest("eth_getWork")

    def submit_work(self, work):
        return self.json.sendJSONRequest("eth_submitWork", work)
