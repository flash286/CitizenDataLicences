import binascii

__author__ = 'nikolas'


class HexUtils:
    @classmethod
    def int_to_hex(cls, number: int) -> str:
        return hex(number)

    @classmethod
    def hex_to_int(cls, number: str) -> int:
        return int(number, 16)

    @classmethod
    def bytes_to_hex(cls, raw: bytes) -> str:
        return binascii.hexlify(raw)

    @classmethod
    def hex_to_bytes(cls, raw: str) -> bytes:
        if raw.startswith('0x'):
            raw = raw[2:]
        return bytes.fromhex(raw)
