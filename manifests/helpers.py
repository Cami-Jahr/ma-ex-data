from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad, pad
import msgpack
import os


KEY = b"/TZh+1VxrtkNiDEH"  # credits yarik0chka
BASE_BODY = {
    "payload": {},  # payload must be filled correctly
    "uuid": "9348356922677091e82fd9f312e54926e4e4fcca4d60783",
    "userId": 335064176361,
    "sessionId": "12c726ff58a228645166d1fef0bf2dba",
    "actionToken": None,
    "ctag": None,
    "actionTime": 133882556400241390,
}


def encrypt_data(data: dict, iv: bytes = os.urandom(16)) -> bytes:
    """Pack dict with msgpack, encrypt with AES-CBC, prepend IV"""
    packed = msgpack.packb(data)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(packed, AES.block_size))
    return iv + ciphertext


def decrypt_data(encrypted_data: bytes) -> dict:
    """Decrypt AES-CBC data and unpack msgpack"""
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return msgpack.unpackb(decrypted)
