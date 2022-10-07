from nacl.bindings.randombytes import randombytes
from nacl.bindings.crypto_scalarmult import crypto_scalarmult_SCALARBYTES, crypto_scalarmult_base, crypto_scalarmult
from nacl.bindings.crypto_aead import crypto_aead_chacha20poly1305_ietf_KEYBYTES, \
    crypto_aead_chacha20poly1305_ietf_encrypt, crypto_aead_chacha20poly1305_ietf_decrypt, \
    crypto_aead_chacha20poly1305_ietf_NPUBBYTES
from nacl.bindings.crypto_generichash import crypto_generichash_BYTES, crypto_generichash_BYTES_MIN, \
    crypto_generichash_BYTES_MAX, crypto_generichash_KEYBYTES_MAX
from nacl.bindings.crypto_generichash import generichash_blake2b_init, generichash_blake2b_update, \
    generichash_blake2b_final


def generichash_blake2b(data: bytes,
                        digest_size: int = crypto_generichash_BYTES,
                        key: bytes = b""
                        ):
    state = generichash_blake2b_init(key=key, digest_size=digest_size)
    generichash_blake2b_update(state, data)
    return generichash_blake2b_final(state)


def crypto_generichash(data: bytes,
                       digest_size: int = crypto_generichash_BYTES,
                       key: bytes = b""):
    return generichash_blake2b(data, digest_size, key)


__all__ = [
    "randombytes",
    "crypto_generichash",
    "crypto_scalarmult_SCALARBYTES",
    "crypto_scalarmult_base",
    "crypto_scalarmult",
    "crypto_aead_chacha20poly1305_ietf_KEYBYTES",
    "crypto_aead_chacha20poly1305_ietf_encrypt",
    "crypto_aead_chacha20poly1305_ietf_decrypt",
    "crypto_generichash_BYTES",
    "crypto_generichash_BYTES_MIN",
    "crypto_generichash_BYTES_MAX",
    "crypto_generichash_KEYBYTES_MAX",
    "crypto_aead_chacha20poly1305_ietf_NPUBBYTES",
]

if __name__ == "__main__":
    skey = randombytes(crypto_scalarmult_SCALARBYTES)
    pkey = crypto_scalarmult_base(skey)
    rskey = randombytes(crypto_scalarmult_SCALARBYTES)
    rpkey = crypto_scalarmult_base(rskey)
    sesskey = crypto_scalarmult(skey, rpkey)
    h = crypto_generichash(sesskey, crypto_generichash_BYTES_MIN)
    odata = b'123'
    nonce = randombytes(crypto_aead_chacha20poly1305_ietf_NPUBBYTES)
    cipherText = crypto_aead_chacha20poly1305_ietf_encrypt(
        odata, None, nonce, sesskey)
    plainText = crypto_aead_chacha20poly1305_ietf_decrypt(
        cipherText, None, nonce, sesskey)
    print(plainText)
