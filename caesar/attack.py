"""Thuật toán tự động phá mã Caesar — brute-force 25 khóa + chấm điểm chi-squared."""
from utils.frequency import letter_frequency, chi_squared_score
from utils.text_utils import clean_text
from caesar.cipher import decrypt


def break_caesar(ciphertext: str) -> tuple[str, int]:
    """Phá mã Caesar bằng brute-force 25 khóa, đánh giá bằng chi-squared.

    Thử tất cả 25 khóa dịch chuyển có thể (1-25), giải mã thử từng khóa,
    tính điểm chi-squared so với tần suất chữ cái tiếng Anh chuẩn,
    rồi chọn khóa cho điểm thấp nhất (giống tiếng Anh nhất).

    Args:
        ciphertext: Văn bản mật mã cần phá.

    Returns:
        Tuple (plaintext, key) — văn bản giải mã và khóa tìm được.

    Ví dụ:
        >>> plaintext, key = break_caesar("KHOOR ZRUOG")
        >>> key
        3
        >>> plaintext
        'HELLO WORLD'
    """
    ciphertext_clean = clean_text(ciphertext)
    if not ciphertext_clean:
        return ciphertext, 0

    best_plaintext = ciphertext
    best_shift = 0
    best_score = float('inf')

    for shift in range(26):
        candidate = decrypt(ciphertext_clean, shift)
        freq = letter_frequency(candidate)
        score = chi_squared_score(freq)

        if score < best_score:
            best_score = score
            best_shift = shift
            best_plaintext = candidate

    return best_plaintext, best_shift
