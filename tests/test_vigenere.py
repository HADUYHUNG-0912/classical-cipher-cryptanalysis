"""Test cho module Vigenère."""
import unittest
from vigenere.cipher import encrypt, decrypt
from vigenere.attack import estimate_key_length, break_vigenere


class TestVigenereCipher(unittest.TestCase):

    def test_encrypt(self):
        self.assertEqual(encrypt("HELLO", "KEY"), "RIJVS")

    def test_decrypt(self):
        self.assertEqual(decrypt("RIJVS", "KEY"), "HELLO")

    def test_encrypt_decrypt_roundtrip(self):
        plaintext = "PYTHONCRYPTOGRAPHYEXAMPLE"
        key = "SECRET"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(decrypt(ciphertext, key), plaintext)

    def test_key_length(self):
        text = encrypt("THISISALONGPLAINTEXTFORTESTINGTOVERIFYTHATTHEVIGENERECIPHERATTACKANDKEYLENGTHESTIMATIONWORKSWELL", "KEY")
        self.assertEqual(estimate_key_length(text), 3)

    def test_break_vigenere(self):
        original_text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHISISALONGTEXTTOENSUREVIGENERECIPHERATTACKWORKSWELLWITHINDEXOFCOINCIDENCE"
        key = "KEY"
        ciphertext = encrypt(original_text, key)
        plaintext, found_key = break_vigenere(ciphertext)
        self.assertEqual(found_key, key)
        self.assertEqual(plaintext, original_text)


if __name__ == '__main__':
    unittest.main()


