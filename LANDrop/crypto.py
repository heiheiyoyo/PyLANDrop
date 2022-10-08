# BSD 3-Clause License
#
# Copyright (c) 2021, LANDrop
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from PyQt6.QtCore import QObject
from LANDrop.sodium import *


class Crypto:
    _inited: bool = False

    @property
    def inited(self) -> bool:
        return Crypto._inited

    @inited.setter
    def inited(self, value: bool) -> None:
        Crypto._inited = value

    def __init__(self) -> None:
        self.sessionKey: bytes = b""
        self.init()
        self.secretKey = randombytes(crypto_scalarmult_SCALARBYTES)
        self.publicKey = crypto_scalarmult_base(self.secretKey)

    @classmethod
    def init(cls) -> None:
        if cls._inited:
            return
        # if sodium_init() == -1:
        #     raise RuntimeError(QObject().tr("Unable to initialize libsodium."))
        cls._inited = True

    def publicKeySize(self) -> int:
        return crypto_aead_chacha20poly1305_ietf_KEYBYTES

    def localPublicKey(self) -> bytes:
        return self.publicKey

    def setRemotePublicKey(self, remotePublicKey: bytes) -> None:
        if not isinstance(remotePublicKey, bytes):
            remotePublicKey = bytes(remotePublicKey)
        try:
            self.sessionKey = crypto_scalarmult(
                self.secretKey, remotePublicKey)
        except RuntimeError:
            raise RuntimeError(QObject().tr(
                "Unable to calculate session key."))

    def sessionKeyDigest(self) -> str:
        h = crypto_generichash(self.sessionKey, crypto_generichash_BYTES_MIN)
        hash_ = 0
        for i in range(8):
            hash_ |= h[i] << (i * 8)
        return f"{hash_ % 1000000:0>6}"

    def encrypt(self, data: bytes) -> bytes:
        if not isinstance(data, bytes):
            data = bytes(data)
        nonce = randombytes(crypto_aead_chacha20poly1305_ietf_NPUBBYTES)
        cipherText = crypto_aead_chacha20poly1305_ietf_encrypt(
            data, None, nonce, self.sessionKey)
        return nonce + cipherText

    def decrypt(self, data: bytes) -> bytes:
        if not isinstance(data, bytes):
            data = bytes(data)
        if len(data) < crypto_aead_chacha20poly1305_ietf_NPUBBYTES:
            raise RuntimeError(QObject().tr(b"Cipher text too short."))
        nonce = data[:crypto_aead_chacha20poly1305_ietf_NPUBBYTES]
        cipherText = data[crypto_aead_chacha20poly1305_ietf_NPUBBYTES:]
        try:
            plainText = crypto_aead_chacha20poly1305_ietf_decrypt(
                cipherText, None, nonce, self.sessionKey)
        except (TypeError, ValueError) as e:
            raise RuntimeError(QObject().tr(
                "Decryption failed.") + " Error: " + str(e))
        return plainText
