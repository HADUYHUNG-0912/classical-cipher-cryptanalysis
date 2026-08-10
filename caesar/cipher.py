"""Mã hóa/giải mã Caesar cipher cơ bản (dùng để tạo ciphertext test)."""


def encrypt(plaintext: str, shift: int) -> str:
    """Mã hóa văn bản bằng Caesar cipher với khóa dịch chuyển shift.

    Chỉ dịch chuyển các chữ cái A-Z, giữ nguyên ký tự khác (số, khoảng trắng...).
    Tự động chuẩn hóa về chữ hoa.

    Args:
        plaintext: Văn bản gốc cần mã hóa.
        shift: Số bước dịch chuyển (0-25). Sẽ được mod 26 tự động.

    Returns:
        Chuỗi đã mã hóa (chữ hoa).

    Ví dụ:
        >>> encrypt("HELLO", 3)
        'KHOOR'
        >>> encrypt("Hello, World!", 13)
        'URYYB, JBEYQ!'
    """
    shift = shift % 26
    result = []
    for ch in plaintext.upper():
        if ch.isalpha():
            shifted = (ord(ch) - ord('A') + shift) % 26
            result.append(chr(shifted + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(ciphertext: str, shift: int) -> str:
    """Giải mã Caesar cipher với khóa dịch chuyển shift.

    Args:
        ciphertext: Văn bản mật mã cần giải mã.
        shift: Số bước dịch chuyển đã dùng khi mã hóa (0-25).

    Returns:
        Văn bản gốc đã giải mã (chữ hoa).

    Ví dụ:
        >>> decrypt("KHOOR", 3)
        'HELLO'
        >>> decrypt("URYYB, JBEYQ!", 13)
        'HELLO, WORLD!'
    """
    return encrypt(ciphertext, -shift)
