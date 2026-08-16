"""Thuật toán tự động phá mã Vigenère — ước lượng độ dài khóa (Kasiski/IC)
rồi tách thành nhiều Caesar con để giải."""
import itertools
from utils.frequency import index_of_coincidence, letter_frequency, ENGLISH_LETTER_FREQ, bigram_log_score
from vigenere.cipher import decrypt


def estimate_key_length(ciphertext: str, max_len: int = 20) -> int:
    """
    Ước lượng độ dài khóa bằng Index of Coincidence.
    """
    ciphertext_clean = ''.join(
        c for c in ciphertext.upper()
        if c.isalpha()
    )

    if len(ciphertext_clean) < 4:
        return 1

    limit = min(max_len, max(1, len(ciphertext_clean) // 3))

    ic_scores = {}
    for key_len in range(1, limit + 1):
        groups = ['' for _ in range(key_len)]

        for i, c in enumerate(ciphertext_clean):
            groups[i % key_len] += c

        avg_ic = sum(
            index_of_coincidence(g)
            for g in groups
        ) / key_len

        ic_scores[key_len] = avg_ic

    high_k = [k for k, score in ic_scores.items() if score >= 0.050]
    if not high_k:
        return max(ic_scores, key=ic_scores.get)

    best_k = high_k[0]
    best_score = -100
    for k in high_k:
        multiples_count = sum(1 for hk in high_k if hk % k == 0)
        score = multiples_count * 10 - k
        if score > best_score:
            best_score = score
            best_k = k

    return best_k


def break_vigenere(ciphertext: str) -> tuple[str, str]:
    """
    1. Gọi estimate_key_length()
    2. Tách ciphertext thành N nhóm ký tự theo vị trí % key_length
    3. Áp dụng thuật toán phá Caesar cho từng nhóm để tìm các ký tự khóa ứng viên
    4. Dùng bigram_log_score để tìm ra khóa và văn bản giải mã tối ưu nhất
    Trả về (plaintext, key)
    """
    ciphertext_clean = ''.join(c for c in ciphertext.upper() if c.isalpha())
    if not ciphertext_clean:
        return ciphertext, ""

    key_length = estimate_key_length(ciphertext)

    candidate_shifts_per_stream = []
    for i in range(key_length):
        group = ciphertext_clean[i::key_length]
        shift_scores = []
        for shift in range(26):
            decrypted_group = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in group)
            freq = letter_frequency(decrypted_group)
            dot = sum(freq.get(ch, 0.0) * ENGLISH_LETTER_FREQ.get(ch, 0.0) for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            shift_scores.append((dot, shift))

        shift_scores.sort(reverse=True)
        top_shifts = [shift_scores[0][1]]
        if len(shift_scores) > 1 and (shift_scores[0][0] - shift_scores[1][0] < 0.5):
            top_shifts.append(shift_scores[1][1])
        candidate_shifts_per_stream.append(top_shifts)

    best_overall_score = -float('inf')
    best_key = ''
    best_plaintext = ciphertext

    for shift_tuple in itertools.product(*candidate_shifts_per_stream):
        cand_key = ''.join(chr(ord('A') + s) for s in shift_tuple)
        cand_plain = decrypt(ciphertext, cand_key)
        bg_score = bigram_log_score(cand_plain)
        if bg_score > best_overall_score:
            best_overall_score = bg_score
            best_key = cand_key
            best_plaintext = cand_plain

    return best_plaintext, best_key



