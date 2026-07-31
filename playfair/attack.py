"""Thuật toán tự động phá mã Playfair — hill-climbing dùng tần suất bigram
(khó nhất trong 3 hệ, không có phân tích tần suất đơn giản)."""
from utils.frequency import chi_squared_score


def score_key(plaintext_guess: str, bigram_freq_table: dict) -> float:
    """TODO: chấm điểm 1 bảng khóa dựa trên độ khớp bigram với tiếng Anh chuẩn."""
    pass


def break_playfair(ciphertext: str, iterations: int = 5000) -> tuple[str, str]:
    """TODO (người phụ trách Playfair implement — phần khó nhất):
    1. Khởi tạo 1 bảng khóa 5x5 ngẫu nhiên
    2. Lặp: hoán đổi ngẫu nhiên 2 ký tự trong bảng, decrypt thử, chấm điểm bigram
    3. Nếu điểm tốt hơn thì giữ, nếu không thì giữ nguyên (hill-climbing)
    4. Lặp lại nhiều lần khởi tạo (random restart) để tránh local optimum
    Trả về (plaintext, key_square_as_string)
    """
    pass
