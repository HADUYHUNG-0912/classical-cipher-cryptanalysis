"""Test đầy đủ cho module Caesar — cipher và attack."""
import unittest
from caesar.cipher import encrypt, decrypt
from caesar.attack import break_caesar


class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_basic(self):
        """Kiểm tra mã hóa cơ bản."""
        self.assertEqual(encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(encrypt("ABC", 1), "BCD")
        self.assertEqual(encrypt("XYZ", 3), "ABC")

    def test_encrypt_with_non_alpha(self):
        """Kiểm tra ký tự không phải chữ cái được giữ nguyên."""
        self.assertEqual(encrypt("Hello, World!", 13), "URYYB, JBEYQ!")
        self.assertEqual(encrypt("A B C", 1), "B C D")

    def test_encrypt_shift_mod(self):
        """Kiểm tra shift tự động mod 26."""
        self.assertEqual(encrypt("HELLO", 29), encrypt("HELLO", 3))
        self.assertEqual(encrypt("HELLO", 0), "HELLO")

    def test_decrypt_basic(self):
        """Kiểm tra giải mã cơ bản."""
        self.assertEqual(decrypt("KHOOR", 3), "HELLO")
        self.assertEqual(decrypt("BCD", 1), "ABC")
        self.assertEqual(decrypt("ABC", 3), "XYZ")

    def test_encrypt_decrypt_roundtrip(self):
        """Kiểm tra mã hóa rồi giải mã trả về văn bản gốc."""
        for shift in range(1, 26):
            plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
            ciphertext = encrypt(plaintext, shift)
            self.assertEqual(decrypt(ciphertext, shift), plaintext, f"Roundtrip thất bại với shift={shift}")

    def test_break_caesar_simple(self):
        """Kiểm tra phá mã với shift nhỏ (dùng văn bản đủ dài để tần suất ổn định)."""
        original = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        key = 3
        ciphertext = encrypt(original, key)
        plaintext, found_key = break_caesar(ciphertext)
        self.assertEqual(found_key, key)
        self.assertEqual(plaintext, original)

    def test_break_caesar_long_text(self):
        """Kiểm tra phá mã với văn bản dài (tần suất chuẩn hơn)."""
        original = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHISISALONGERTEXTTOMAKEFREQUENCYANALYSISMOREACCURATE"
        key = 7
        ciphertext = encrypt(original, key)
        plaintext, found_key = break_caesar(ciphertext)
        self.assertEqual(found_key, key)
        self.assertEqual(plaintext, original)

    def test_break_caesar_all_shifts(self):
        """Kiểm tra phá mã với mọi khóa từ 1-25."""
        original = "CRYPTOGRAPHYISTHEPRACTICEANDSTUDYOFTECHNIQUESFOR"
        for key in range(1, 26):
            ciphertext = encrypt(original, key)
            plaintext, found_key = break_caesar(ciphertext)
            self.assertEqual(found_key, key, f"Phá mã thất bại với key={key}, tìm ra={found_key}")


if __name__ == '__main__':
    unittest.main()

