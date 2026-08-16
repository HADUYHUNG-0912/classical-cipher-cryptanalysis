import unittest
from playfair.cipher import encrypt, decrypt, generate_key_square, prepare_plaintext


class TestPlayfairCipher(unittest.TestCase):

    def test_generate_key_square(self):
        key = "MONARCHY"
        square = generate_key_square(key)

        # Kiểm tra kích thước 5x5
        self.assertEqual(len(square), 5)
        for row in square:
            self.assertEqual(len(row), 5)

        # Tổng số ký tự độc nhất = 25 (không chứa 'J')
        flat = [ch for row in square for ch in row]
        self.assertEqual(len(flat), 25)
        self.assertEqual(len(set(flat)), 25)
        self.assertNotIn('J', flat)

        # Kiểm tra các chữ cái của khóa đứng trước
        expected_start = ['M', 'O', 'N', 'A', 'R', 'C', 'H', 'Y']
        self.assertEqual(flat[:8], expected_start)

    def test_encrypt_decrypt_roundtrip(self):
        key = "PLAYFAIR"
        plaintext = "INSTRUMENTS"

        ciphertext = encrypt(plaintext, key)
        self.assertEqual(len(ciphertext) % 2, 0)

        decrypted = decrypt(ciphertext, key)
        prepared = prepare_plaintext(plaintext)
        self.assertEqual(decrypted, prepared)

    def test_playfair_known_vector(self):
        # Ví dụ Playfair: Key = MONARCHY, Plaintext = INSTRUMENTS
        # Prepared: IN ST RU ME NT SX -> Ciphertext: GATLMZCLRQXA
        key = "MONARCHY"
        plaintext = "INSTRUMENTS"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "GATLMZCLRQXA")

        decrypted = decrypt(ciphertext, key)
        self.assertEqual(decrypted, "INSTRUMENTSX")

    def test_break_playfair(self):
        from playfair.attack import break_playfair
        key = "KEYWORD"
        plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        ciphertext = encrypt(plaintext, key)

        # Chạy thử với 500 iterations, 2 restarts để đảm bảo hàm attack không bị lỗi runtime
        decrypted_guess, best_key = break_playfair(ciphertext, iterations=500, restarts=2)
        self.assertEqual(len(decrypted_guess), len(ciphertext))

    def test_break_playfair_long_text(self):
        from playfair.attack import break_playfair, score_key
        key = "SECRETKEY"
        plaintext = (
            "IT WAS THE BEST OF TIMES IT WAS THE WORST OF TIMES IT WAS THE AGE OF WISDOM "
            "IT WAS THE AGE OF FOOLISHNESS IT WAS THE EPOCH OF BELIEF IT WAS THE EPOCH OF INCREDULITY "
            "IT WAS THE SEASON OF LIGHT IT WAS THE SEASON OF DARKNESS IT WAS THE SPRING OF HOPE "
            "IT WAS THE WINTER OF DESPAIR WE HAD EVERYTHING BEFORE US WE HAD NOTHING BEFORE US"
        )
        ciphertext = encrypt(plaintext, key)
        self.assertGreater(len(ciphertext), 200)

        # Chạy phá mã Playfair bằng Simulated Annealing
        decrypted_guess, best_key = break_playfair(ciphertext, iterations=5000, restarts=3)
        self.assertEqual(len(decrypted_guess), len(ciphertext))
        # Kiểm tra điểm số bigram của kết quả đoán vượt trội hơn điểm số chuỗi ngẫu nhiên
        score_decrypted = score_key(decrypted_guess)
        score_cipher = score_key(ciphertext)
        self.assertGreater(score_decrypted, score_cipher)

    def test_package_exports(self):
        # Kiểm tra import trực tiếp từ package playfair qua __init__.py
        import playfair
        self.assertTrue(callable(playfair.encrypt))
        self.assertTrue(callable(playfair.decrypt))
        self.assertTrue(callable(playfair.generate_key_square))
        self.assertTrue(callable(playfair.break_playfair))


if __name__ == '__main__':
    unittest.main()




