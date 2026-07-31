"""Các hàm phân tích tần suất dùng chung cho attack.py của 3 module."""


def letter_frequency(text: str) -> dict:
    """Tính tần suất xuất hiện từng chữ cái trong văn bản (%)."""
    # TODO: implement
    pass


def chi_squared_score(observed_freq: dict, expected_freq: dict) -> float:
    """Tính chi-squared statistic giữa tần suất quan sát và tần suất chuẩn tiếng Anh.
    Điểm càng thấp càng giống tiếng Anh thật."""
    # TODO: implement
    pass


def index_of_coincidence(text: str) -> float:
    """Tính Index of Coincidence (IC) của văn bản — dùng để ước lượng độ dài khóa Vigenère."""
    # TODO: implement
    pass
