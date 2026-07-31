"""Các hàm tiện ích xử lý văn bản dùng chung cho cả 3 module Caesar, Vigenère, Playfair."""


def clean_text(text: str) -> str:
    """Chuẩn hóa văn bản: viết hoa toàn bộ, chỉ giữ lại chữ cái A-Z.

    Ví dụ:
        >>> clean_text("Hello, World! 123")
        'HELLOWORLD'
        >>> clean_text("the quick brown fox")
        'THEQUICKBROWNFOX'
    """
    return ''.join(ch.upper() for ch in text if ch.isalpha())


def read_file(path: str) -> str:
    """Đọc nội dung file văn bản và trả về chuỗi string.

    Args:
        path: Đường dẫn tuyệt đối hoặc tương đối đến file.

    Returns:
        Nội dung file dưới dạng chuỗi. Trả về chuỗi rỗng nếu file không tồn tại.

    Ví dụ:
        >>> content = read_file("data/sample_corpus.txt")
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[read_file] Không tìm thấy file: {path}")
        return ""
    except Exception as e:
        print(f"[read_file] Lỗi đọc file {path}: {e}")
        return ""


def write_file(path: str, content: str) -> None:
    """Ghi nội dung ra file văn bản (tạo mới hoặc ghi đè).

    Args:
        path: Đường dẫn tuyệt đối hoặc tương đối đến file.
        content: Nội dung cần ghi.

    Ví dụ:
        >>> write_file("output/result.txt", "KHOA LA: 3")
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"[write_file] Lỗi ghi file {path}: {e}")
