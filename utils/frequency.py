"""Các hàm phân tích tần suất dùng chung cho attack.py của cả 3 module."""

import json
import os


# Tải bảng tần suất chữ cái tiếng Anh chuẩn từ file data/
_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
_LETTER_FREQ_PATH = os.path.join(_DATA_DIR, 'english_letter_freq.json')
_BIGRAM_FREQ_PATH = os.path.join(_DATA_DIR, 'english_bigram_freq.json')

def _load_json(path: str) -> dict:
    """Tải dữ liệu JSON từ file, trả về dict rỗng nếu lỗi."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[frequency] Không tải được dữ liệu từ {path}: {e}")
        return {}

ENGLISH_LETTER_FREQ: dict = _load_json(_LETTER_FREQ_PATH)
ENGLISH_BIGRAM_FREQ: dict = _load_json(_BIGRAM_FREQ_PATH)


def letter_frequency(text: str) -> dict:
    """Tính tần suất xuất hiện (%) của từng chữ cái A-Z trong văn bản.

    Chỉ đếm các chữ cái (A-Z), bỏ qua ký tự khác.
    Tổng các giá trị trả về = 100.0 (nếu text không rỗng).

    Args:
        text: Văn bản đã được chuẩn hóa (nên dùng clean_text() trước).

    Returns:
        Dict {chữ_cái: tần_suất_%}, ví dụ: {'A': 8.17, 'B': 1.49, ...}

    Ví dụ:
        >>> letter_frequency("HELLO")
        {'H': 20.0, 'E': 20.0, 'L': 40.0, 'O': 20.0, ...}
    """
    text = text.upper()
    letters_only = [ch for ch in text if ch.isalpha()]
    total = len(letters_only)
    if total == 0:
        return {chr(i): 0.0 for i in range(ord('A'), ord('Z') + 1)}

    counts = {chr(i): 0 for i in range(ord('A'), ord('Z') + 1)}
    for ch in letters_only:
        counts[ch] += 1

    return {ch: (count / total) * 100 for ch, count in counts.items()}


def chi_squared_score(observed_freq: dict, expected_freq: dict = None) -> float:
    """Tính điểm Chi-squared (χ²) giữa tần suất quan sát và tần suất chuẩn tiếng Anh.

    Điểm càng THẤP thì văn bản càng GIỐNG tiếng Anh thật.
    Dùng để so sánh các kết quả giải mã thử và chọn ra cái tốt nhất.

    Công thức:
        χ² = Σ (Oi - Ei)² / Ei
        Trong đó: Oi = tần suất quan sát, Ei = tần suất kỳ vọng tiếng Anh

    Args:
        observed_freq: Dict tần suất (%) của văn bản cần đánh giá.
        expected_freq: Dict tần suất chuẩn tiếng Anh. Nếu None thì dùng bảng mặc định.

    Returns:
        Điểm chi-squared (float). Giá trị càng thấp thì văn bản càng khớp tiếng Anh.

    Ví dụ:
        >>> freq = letter_frequency("SOME DECRYPTED TEXT")
        >>> score = chi_squared_score(freq)
        >>> # score thấp → nhiều khả năng là tiếng Anh thật
    """
    if expected_freq is None:
        expected_freq = ENGLISH_LETTER_FREQ

    score = 0.0
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = observed_freq.get(letter, 0.0)
        expected = expected_freq.get(letter, 0.001)  # tránh chia cho 0
        score += (observed - expected) ** 2 / expected

    return score


def index_of_coincidence(text: str) -> float:
    """Tính chỉ số IC (Index of Coincidence) của văn bản.

    IC đo xác suất 2 ký tự ngẫu nhiên được chọn từ văn bản là giống nhau.
    - Tiếng Anh tự nhiên: IC ≈ 0.067
    - Văn bản ngẫu nhiên hoàn toàn: IC ≈ 0.038
    → Dùng để phát hiện độ dài khóa Vigenère: ghép ký tự theo từng vị trí mod m,
      nếu IC ≈ 0.067 thì m đúng là độ dài khóa.

    Công thức:
        IC = Σ [ni * (ni - 1)] / [N * (N - 1)]
        Trong đó: ni = số lần xuất hiện chữ cái i, N = tổng số chữ cái

    Args:
        text: Văn bản cần tính IC (nên đã được chuẩn hóa A-Z).

    Returns:
        Giá trị IC (float trong khoảng 0.038 - 0.067 với văn bản tiếng Anh).

    Ví dụ:
        >>> ic = index_of_coincidence("THEQUICKBROWNFOX")
        >>> # ic ≈ 0.067 với văn bản tiếng Anh tự nhiên
    """
    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    n = len(text)
    if n < 2:
        return 0.0

    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1

    numerator = sum(count * (count - 1) for count in freq.values())
    denominator = n * (n - 1)

    return numerator / denominator


def bigram_frequency(text: str) -> dict:
    """Tính tần suất (%) các cặp ký tự (bigram) trong văn bản.

    Dùng riêng cho Playfair attack (hill-climbing) để đánh giá chất lượng giải mã.

    Args:
        text: Văn bản đã được chuẩn hóa A-Z (không có khoảng trắng).

    Returns:
        Dict {bigram: tần_suất_%}, ví dụ: {'TH': 3.56, 'HE': 3.07, ...}

    Ví dụ:
        >>> bigram_frequency("THEQUICK")
        {'TH': 12.5, 'HE': 12.5, 'EQ': 12.5, ...}
    """
    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    total_bigrams = len(text) - 1
    if total_bigrams <= 0:
        return {}

    counts = {}
    for i in range(total_bigrams):
        bigram = text[i:i+2]
        counts[bigram] = counts.get(bigram, 0) + 1

    return {bigram: (count / total_bigrams) * 100 for bigram, count in counts.items()}


def bigram_log_score(text: str, bigram_table: dict = None, step: int = 1) -> float:
    """Chấm điểm văn bản dựa trên log-likelihood của bigram frequency.

    Dùng cho Playfair attack (non-overlapping digraphs khi step=2) hoặc Vigenère.
    Điểm càng CAO thì văn bản càng GIỐNG tiếng Anh (ngược với chi-squared).

    Args:
        text: Văn bản cần đánh giá.
        bigram_table: Bảng tần suất bigram tham chiếu. Nếu None thì dùng bảng mặc định.
        step: Bước nhảy khi đọc cặp ký tự (1 cho overlapping bigram, 2 cho non-overlapping digraph).

    Returns:
        Tổng log-likelihood score (float âm, gần 0 hơn = tốt hơn).
    """
    import math
    if bigram_table is None:
        bigram_table = ENGLISH_BIGRAM_FREQ

    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    score = 0.0
    floor_prob = 0.01  # xác suất tối thiểu cho bigram không có trong bảng

    for i in range(0, len(text) - 1, step):
        bigram = text[i:i+2]
        prob = bigram_table.get(bigram, floor_prob)
        score += math.log10(prob / 100.0)  # chuyển % → xác suất rồi lấy log

    return score
