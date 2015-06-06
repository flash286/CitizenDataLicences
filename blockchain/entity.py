import json
import binascii
from ethereum.abi import ContractTranslator
from blockchain.jsonrpc.ethereum import EthereumAPI

__author__ = 'nikolas'


class Contract:
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

    def bytes_to_hex(self, raw):
        return binascii.hexlify(raw)

    @property
    def addr(self):
        return self._addr[2:]

    @property
    def abi(self):
        return self._abi

    @property
    def transport(self):
        if not self._transport or not isinstance(self._transport, EthereumAPI):
            self._transport = EthereumAPI()
        return self._transport

    def call(self, method_name,  *args):
        if method_name not in self.abi.function_data:
            raise NotImplementedError("This method does not exists in {}".format(self.abi))

        if len(args) != len(self.abi.function_data[method_name]['signature']):
            raise TypeError("Method {} receive {} args, but we send {}".format(
                method_name,
                len(self.abi.function_data[method_name]['signature']),
                len(args)
            ))

        call_data = self.abi.encode(method_name, args)
        call_data = self.bytes_to_hex(call_data)
        call_data = call_data.decode("ascii")

        result_rpc = self.transport.call(self.addr, call_data)

        return result_rpc

    def balance(self):
        raise NotImplementedError()
