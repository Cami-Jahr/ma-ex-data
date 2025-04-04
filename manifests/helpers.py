import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import msgpack

url = "https://api-gl.mmme.pokelabo.jp/api/akamai/create_token"
key = b"/TZh+1VxrtkNiDEH"  # credits yarik0chka
headers = {
    "Host": "api-gl.mmme.pokelabo.jp",
    "Accept": "*/*",
    "Content-Type": "application/x-msgpack",
    "x-region": "AU",
    "x-language": "en-Latn",
    "x-timezone-offset": "-14400",
    "x-app-version": "1.0.1",
    "X-post-signature": "2DlXpy5aeOO3HiBaIPv4l+bUcxthxXtf0qRT4lduPdbNj5aoEXeOSxgkDl/hXjiH/71gQLX3b2X+WBsgyYzAnA==",
    "X-Unity-Version": "2022.3.21f1",
}
# TO MAKE x-post-signature: https://discordapp.com/channels/603359898507673630/1353944587286216705/1357607580100333570


def decrypt_data(encrypted_data: bytes) -> dict:
    """Decrypt AES-CBC data and unpack msgpack"""
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return msgpack.unpackb(decrypted)


encrypted_request = bytes.fromhex(
    """
88 46 51 55 30 61 67 82 55 2C AB 5E 1D 7C 85 0F
A3 CF BB B2 1E 66 0D C1 BA F0 5C 6C 89 DD 94 D7
A3 A7 E7 8A F6 64 2F 80 5B DC EC 4E EF D8 3D FF
C8 60 3E D3 56 18 D2 5B D1 91 13 55 F4 11 AC 17
42 7A 5F A2 51 BA 48 F8 1E D6 A8 D6 A9 3E 31 56
81 CB 5E 4A 7A 3E 80 0D CF 31 9A AE E9 BD 50 66
A7 04 DF 95 40 E8 E1 43 0A 58 24 2C 0A F8 B4 C2
DA 6B 55 02 FD F9 BA 59 51 82 DB F0 27 F5 E1 BD
A0 E2 A9 A9 8A 27 0D D2 39 CF F1 A7 DD 67 D1 F2
B2 1C 95 1F C1 C6 4D C7 CB 84 F5 42 78 8D 26 34
84 F6 D0 D3 65 03 ED CA A9 09 5D B8 06 4E 8D 29
6B 94 20 9E F8 6F 5B EB 36 16 48 B9 9A 0E 33 18
06 E9 A5 D6 6C B2 2E E7 3B 65 17 CC 8F 50 2F 79
EE 15 16 78 E0 73 E5 4E AE 43 AF 39 92 0F 8A DE
80 59 3E 11 48 34 2D B4 EC 74 98 16 CB 86 66 82
49 CC 94 7C F9 04 00 2E D8 C9 91 A8 F1 13 3A 69
F4 9C D7 F4 6D 30 C0 42 E7 BC 73 3C 40 13 15 DB
A6 E4 A9 5B C4 B3 55 E8 50 A2 9E 98 38 F3 DF 67
"""
)
encrypted_request = bytes.fromhex(
    """8846515530616782552cab5e1d7c850fa3cfbbb21e660dc1baf05c6c89dd94d7a3a7e78af6642f805bdcec4eefd83dffc8603ed35618d25bd1911355f411ac17d4b274fbd6f5fa5bb4c30522b2c0555b459208520794c6b5cdb7c5b00fc5cd3c748dc323e94cbc5d37479d66a11141f06cea3c3d7814f422fa20303f16bfb9e22b86ccf0027c837702e44b958ed4d658038e0b315c2d12d8700a42ee92eb68f7bebd9810d6bd1f0f16dc412b8bd05321020a38786d5cc9b9e23565396411c6b5641f2f6014e7850b4a6c1fcba2a9216bd40a1c19f7eb433a9332ca7f272c59bfb3fc44f7f64592db5d8081abddbce5d69ece72c18a5166920faa0e34887369dc8354b3ae3ab05b4439fda69bd9bfa2235725221a6b04336fcab15c468938ab44"""
)
print(decrypt_data(encrypted_request))
def get_token():
    response = requests.post(url, headers=headers, data=encrypted_request)
    response.raise_for_status()
    return decrypt_data(response.content).get("payload", {}).get("token")
