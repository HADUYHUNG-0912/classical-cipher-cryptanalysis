from utils.text_utils import clean_text

def generate_key_square(key: str) -> list[list[str]]:
    """Tạo bảng ma trận 5x5 từ khóa. Gộp 'J' vào 'I'."""
    cleaned_key = clean_text(key).replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  

    used = set()
    square_flat = []

    for ch in cleaned_key:
        if ch not in used and ch in alphabet:
            used.add(ch)
            square_flat.append(ch)

    for ch in alphabet:
        if ch not in used:
            used.add(ch)
            square_flat.append(ch)

    return [square_flat[i:i + 5] for i in range(0, 25, 5)]


def _build_pos_map(key_square: list[list[str]]) -> dict[str, tuple[int, int]]:
    """Tạo map vị trí (row, col) cho từng ký tự trong bảng 5x5."""
    pos_map = {}
    for r in range(5):
        for c in range(5):
            pos_map[key_square[r][c]] = (r, c)
    return pos_map


def prepare_plaintext(plaintext: str) -> str:
    text = clean_text(plaintext).replace('J', 'I')
    if not text:
        return ""

    prepared = []
    i = 0
    while i < len(text):
        c1 = text[i]
        if i + 1 < len(text):
            c2 = text[i + 1]
            if c1 == c2:
                pad = 'Q' if c1 == 'X' else 'X'
                prepared.extend([c1, pad])
                i += 1
            else:
                prepared.extend([c1, c2])
                i += 2
        else:
            pad = 'Q' if c1 == 'X' else 'X'
            prepared.extend([c1, pad])
            i += 1

    return "".join(prepared)


def encrypt(plaintext: str, key: str) -> str:
    key_square = generate_key_square(key)
    pos_map = _build_pos_map(key_square)
    prep_text = prepare_plaintext(plaintext)

    ciphertext = []
    for i in range(0, len(prep_text), 2):
        c1, c2 = prep_text[i], prep_text[i + 1]
        r1, col1 = pos_map[c1]
        r2, col2 = pos_map[c2]

        if r1 == r2:
            # Cùng hàng -> dịch phải
            ciphertext.append(key_square[r1][(col1 + 1) % 5])
            ciphertext.append(key_square[r2][(col2 + 1) % 5])
        elif col1 == col2:
            # Cùng cột -> dịch xuống
            ciphertext.append(key_square[(r1 + 1) % 5][col1])
            ciphertext.append(key_square[(r2 + 1) % 5][col2])
        else:
            # Hình chữ nhật -> đổi cột
            ciphertext.append(key_square[r1][col2])
            ciphertext.append(key_square[r2][col1])

    return "".join(ciphertext)


def decrypt(ciphertext: str, key: str) -> str:
    cleaned_cipher = clean_text(ciphertext).replace('J', 'I')
    if len(cleaned_cipher) % 2 != 0:
        cleaned_cipher += 'X'

    key_square = generate_key_square(key)
    pos_map = _build_pos_map(key_square)

    plaintext = []
    for i in range(0, len(cleaned_cipher), 2):
        c1, c2 = cleaned_cipher[i], cleaned_cipher[i + 1]
        r1, col1 = pos_map[c1]
        r2, col2 = pos_map[c2]

        if r1 == r2:
            # Cùng hàng -> dịch trái
            plaintext.append(key_square[r1][(col1 - 1) % 5])
            plaintext.append(key_square[r2][(col2 - 1) % 5])
        elif col1 == col2:
            # Cùng cột -> dịch lên
            plaintext.append(key_square[(r1 - 1) % 5][col1])
            plaintext.append(key_square[(r2 - 1) % 5][col2])
        else:
            # Hình chữ nhật -> đổi cột
            plaintext.append(key_square[r1][col2])
            plaintext.append(key_square[r2][col1])

    return "".join(plaintext)

