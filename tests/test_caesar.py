"""Test đầy đủ cho module Caesar — cipher và attack."""
from caesar.cipher import encrypt, decrypt
from caesar.attack import break_caesar


def test_encrypt_basic():
    """Kiểm tra mã hóa cơ bản."""
    assert encrypt("HELLO", 3) == "KHOOR"
    assert encrypt("ABC", 1) == "BCD"
    assert encrypt("XYZ", 3) == "ABC"


def test_encrypt_with_non_alpha():
    """Kiểm tra ký tự không phải chữ cái được giữ nguyên."""
    assert encrypt("Hello, World!", 13) == "URYYB, JBEYQ!"
    assert encrypt("A B C", 1) == "B C D"


def test_encrypt_shift_mod():
    """Kiểm tra shift tự động mod 26."""
    assert encrypt("HELLO", 29) == encrypt("HELLO", 3)
    assert encrypt("HELLO", 0) == "HELLO"


def test_decrypt_basic():
    """Kiểm tra giải mã cơ bản."""
    assert decrypt("KHOOR", 3) == "HELLO"
    assert decrypt("BCD", 1) == "ABC"
    assert decrypt("ABC", 3) == "XYZ"


def test_encrypt_decrypt_roundtrip():
    """Kiểm tra mã hóa rồi giải mã trả về văn bản gốc."""
    for shift in range(1, 26):
        plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        ciphertext = encrypt(plaintext, shift)
        assert decrypt(ciphertext, shift) == plaintext, f"Roundtrip thất bại với shift={shift}"


def test_break_caesar_simple():
    """Kiểm tra phá mã với shift nhỏ (dùng văn bản đủ dài để tần suất ổn định)."""
    original = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 3
    ciphertext = encrypt(original, key)
    plaintext, found_key = break_caesar(ciphertext)
    assert found_key == key
    assert plaintext == original


def test_break_caesar_long_text():
    """Kiểm tra phá mã với văn bản dài (tần suất chuẩn hơn)."""
    original = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHISISALONGERTEXTTOMAKEFREQUENCYANALYSISMOREACCURATE"
    key = 7
    ciphertext = encrypt(original, key)
    plaintext, found_key = break_caesar(ciphertext)
    assert found_key == key
    assert plaintext == original


def test_break_caesar_all_shifts():
    """Kiểm tra phá mã với mọi khóa từ 1-25."""
    original = "CRYPTOGRAPHYISTHEPRACTICEANDSTUDYOFTECHNIQUESFOR"
    for key in range(1, 26):
        ciphertext = encrypt(original, key)
        plaintext, found_key = break_caesar(ciphertext)
        assert found_key == key, f"Phá mã thất bại với key={key}, tìm ra={found_key}"
