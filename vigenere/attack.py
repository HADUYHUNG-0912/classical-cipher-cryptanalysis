"""Thuật toán tự động phá mã Vigenère — ước lượng độ dài khóa (Kasiski/IC)
rồi tách thành nhiều Caesar con để giải."""
from utils.frequency import index_of_coincidence


def estimate_key_length(ciphertext: str, max_len: int = 20) -> int:
    """TODO (người phụ trách Vigenère implement):
    Dùng Kasiski Examination hoặc Index of Coincidence để đoán độ dài khóa."""
    pass


def break_vigenere(ciphertext: str) -> tuple[str, str]:
    """TODO:
    1. Gọi estimate_key_length()
    2. Tách ciphertext thành N nhóm ký tự theo vị trí % key_length
    3. Áp dụng thuật toán phá Caesar cho từng nhóm để tìm từng ký tự khóa
    4. Ghép khóa lại, giải mã toàn bộ văn bản
    Trả về (plaintext, key)
    """
    pass
