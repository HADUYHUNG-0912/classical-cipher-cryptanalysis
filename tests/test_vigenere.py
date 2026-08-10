"""Test cho module Vigenère."""
from vigenere.cipher import encrypt, decrypt
from vigenere.attack import estimate_key_length, break_vigenere


def test_encrypt():
    assert encrypt("HELLO", "KEY") == "RIJVS"


def test_decrypt():
    assert decrypt("RIJVS", "KEY") == "HELLO"


def test_encrypt_decrypt_roundtrip():
    plaintext = "PYTHONCRYPTOGRAPHYEXAMPLE"
    key = "SECRET"
    ciphertext = encrypt(plaintext, key)
    assert decrypt(ciphertext, key) == plaintext


def test_key_length():
    text = encrypt("THISISALONGPLAINTEXTFORTESTINGTOVERIFYTHATTHEVIGENERECIPHERATTACKANDKEYLENGTHESTIMATIONWORKSWELL", "KEY")
    assert estimate_key_length(text) == 3



def test_break_vigenere():
    original_text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHISISALONGTEXTTOENSUREVIGENERECIPHERATTACKWORKSWELLWITHINDEXOFCOINCIDENCE"
    key = "KEY"
    ciphertext = encrypt(original_text, key)
    plaintext, found_key = break_vigenere(ciphertext)
    assert found_key == key
    assert plaintext == original_text

