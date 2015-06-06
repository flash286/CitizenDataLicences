import binascii

__author__ = 'nikolas'


class HexUtils:
    def int_to_hex(self, number):
        return str(hex(number))

    def hex_to_int(self, number):
        return int(number, 16)

    def bytes_to_hex(self, raw):
        return binascii.hexlify(raw)

    def hex_to_bytes(self):
        pass
