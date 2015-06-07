import json
import binascii
from ethereum.abi import ContractTranslator
from blockchain.jsonrpc.ethereum import EthereumAPI
from common.utils import HexUtils

__author__ = 'nikolas'


class Contract(HexUtils):

    DEFAULT_GAS_PRRICE = "0x9184e72a000"
    DEFAULT_GAS = "0x1b7740"

    _addr = None
    _abi = None
    _transport = None

    def __init__(self, addr, abi):
        self._addr = addr
        self._abi = self._parse_abi(abi)

    def _parse_abi(self, raw_abi):

        assert isinstance(raw_abi, str)

        abi = json.loads(raw_abi)
        for i, entity in enumerate(abi):
            if entity['type'] == 'constructor':  # Current implementation of ABI don't understand solidity constructor
                del (abi[i])
        raw = json.dumps(abi)
        translator = ContractTranslator(raw.encode("ascii"))

        assert isinstance(translator.event_data, dict)
        assert isinstance(translator.function_data, dict)

        return translator

    @property
    def addr(self):
        return self._addr

    @property
    def abi(self):
        return self._abi

    @property
    def transport(self):
        if not self._transport or not isinstance(self._transport, EthereumAPI):
            self._transport = EthereumAPI()
        return self._transport

    def _validate_method(self, method_name, *args):
        if method_name not in self.abi.function_data:
            raise NotImplementedError("This method does not exists in {}".format(self.abi))

        if len(args) != len(self.abi.function_data[method_name]['signature']):
            raise TypeError("Method {} receive {} args, but we send {}".format(
                method_name,
                len(self.abi.function_data[method_name]['signature']),
                len(args)
            ))

    def get_data_for_method_call(self, method_name, *args):
        call_data = self.abi.encode(method_name, args)
        call_data = self.bytes_to_hex(call_data)
        return "0x{}".format(call_data.decode("ascii"))

    def transact(self, from_addr, method_name, *args, value=0):
        self._validate_method(method_name, *args)
        data = self.get_data_for_method_call(method_name, *args)
        params = dict(
            from_addr=from_addr,
            to_addr=self.addr,
            gas=self.DEFAULT_GAS,
            gasPrice=self.DEFAULT_GAS_PRRICE,
            value=self.int_to_hex(value),
            data=data
        )
        result = self.transport.send_transaction(**params)
        return result

    def call(self, from_addr, method_name, *args):
        self._validate_method(method_name, *args)
        data = self.get_data_for_method_call(method_name, *args)

        params = {
            "from": from_addr,
            "to": self.addr,
            "gas": self.int_to_hex(0),
            "gasPrice": self.DEFAULT_GAS_PRRICE,
            "data": data
        }
        result_rpc = self.transport.call(params)
        result_rpc = self.abi.decode(method_name, self.hex_to_bytes(result_rpc))
        return result_rpc

    def balance(self, owner=None):
        if not owner:
            owner = self.addr
        result_rpc = self.transport.balance_at(owner)
        return self.hex_to_int(result_rpc)
