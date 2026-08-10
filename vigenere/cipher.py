"""Mã hóa/giải mã Vigenère cipher cơ bản."""


def encrypt(plaintext: str, key: str) -> str:
    plaintext = plaintext.upper()
    key = key.upper()

    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            p = ord(char) - ord('A')
            k = ord(key[key_index % len(key)]) - ord('A')
            c = (p + k) % 26
            ciphertext += chr(c + ord('A'))
            key_index += 1
        else:
            ciphertext += char

    return ciphertext


def decrypt(ciphertext: str, key: str) -> str:
    ciphertext = ciphertext.upper()
    key = key.upper()

    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            c = ord(char) - ord('A')
            k = ord(key[key_index % len(key)]) - ord('A')
            p = (c - k) % 26
            plaintext += chr(p + ord('A'))
            key_index += 1
        else:
            plaintext += char

    return plaintext

