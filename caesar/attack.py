"""Thuật toán tự động phá mã Caesar — brute-force 25 khóa + chấm điểm chi-squared."""
from utils.frequency import letter_frequency, chi_squared_score
from utils.text_utils import clean_text


def break_caesar(ciphertext: str) -> tuple[str, int]:
    """Thử tất cả 25 khóa dịch, trả về (plaintext, key) có chi-squared thấp nhất.
    TODO (người phụ trách Caesar implement):
    1. Với mỗi shift từ 0-25, decrypt thử
    2. Tính chi-squared so với tần suất tiếng Anh chuẩn
    3. Trả về kết quả có điểm thấp nhất (giống tiếng Anh nhất)
    """
    pass
