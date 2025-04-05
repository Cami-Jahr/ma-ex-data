import requests
from helpers import decrypt_data


def get_token(is_en=True):
    url = "https://api-gl.mmme.pokelabo.jp/api/akamai/create_token"
    headers = {
        "x-language": "en-Latn" if is_en else "ja-Jpan",
        "X-post-signature": "2DlXpy5aeOO3HiBaIPv4l+bUcxthxXtf0qRT4lduPdbNj5aoEXeOSxgkDl/hXjiH/71gQLX3b2X+WBsgyYzAnA==",
    }
    data = bytes.fromhex(
        "8846515530616782552cab5e1d7c850fa3cfbbb21e660dc1baf05c6c89dd94d7a3a7e78af6642f805bdcec4eefd83dffc8603ed35618d25bd1911355f411ac17d4b274fbd6f5fa5bb4c30522b2c0555b459208520794c6b5cdb7c5b00fc5cd3c748dc323e94cbc5d37479d66a11141f06cea3c3d7814f422fa20303f16bfb9e22b86ccf0027c837702e44b958ed4d658038e0b315c2d12d8700a42ee92eb68f7bebd9810d6bd1f0f16dc412b8bd05321020a38786d5cc9b9e23565396411c6b5641f2f6014e7850b4a6c1fcba2a9216bd40a1c19f7eb433a9332ca7f272c59bfb3fc44f7f64592db5d8081abddbce5d69ece72c18a5166920faa0e34887369dc8354b3ae3ab05b4439fda69bd9bfa2235725221a6b04336fcab15c468938ab44"
    )

    response = requests.post(url, headers=headers, data=data)

    response.raise_for_status()
    return decrypt_data(response.content).get("payload", {}).get("token")
