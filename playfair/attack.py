import math
import random
from playfair.cipher import decrypt, generate_key_square
from utils.frequency import ENGLISH_BIGRAM_FREQ, bigram_log_score
from utils.text_utils import clean_text

ALPHABET_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def score_key(plaintext_guess: str, bigram_freq_table: dict = None) -> float:
    """Chấm điểm văn bản bằng non-overlapping digraphs"""
    return bigram_log_score(plaintext_guess, bigram_freq_table, step=2)


def _mutate_key(key: str) -> str:
    key_list = list(key)
    choice = random.random()

    if choice < 0.70:
        # Swap 2 ký tự ngẫu nhiên
        i, j = random.sample(range(25), 2)
        key_list[i], key_list[j] = key_list[j], key_list[i]
    elif choice < 0.85:
        # Swap 2 hàng
        r1, r2 = random.sample(range(5), 2)
        for c in range(5):
            key_list[r1 * 5 + c], key_list[r2 * 5 + c] = key_list[r2 * 5 + c], key_list[r1 * 5 + c]
    elif choice < 0.95:
        # Swap 2 cột
        c1, c2 = random.sample(range(5), 2)
        for r in range(5):
            key_list[r * 5 + c1], key_list[r * 5 + c2] = key_list[r * 5 + c2], key_list[r * 5 + c1]
    else:
        # Đảo ngược bảng khóa
        key_list.reverse()

    return "".join(key_list)


def break_playfair(
    ciphertext: str,
    iterations: int = 10000,
    restarts: int = 10,
    bigram_table: dict = None
) -> tuple[str, str]:
    """Phá mã Playfair tự động 
    bằng Simulated Annealing kết hợp Random Restart.

    Args:
        ciphertext: Văn bản mật mã.
        iterations: Số vòng lặp annealing cho mỗi lần restart (mặc định 10000).
        restarts: Số lần khởi tạo ngẫu nhiên (mặc định 10).
        bigram_table: Bảng tần suất bigram tham chiếu.

    Returns:
        Tuple (plaintext_đoán_được, key_đoán_được)
    """
    cleaned_cipher = clean_text(ciphertext).replace('J', 'I')
    if not cleaned_cipher:
        return "", ALPHABET_25

    if bigram_table is None:
        bigram_table = ENGLISH_BIGRAM_FREQ

    best_global_score = float('-inf')
    best_global_key = ALPHABET_25
    best_global_plaintext = ""

    # Tham số Simulated Annealing
    temp_start = 20.0
    temp_end = 0.05

    # Thực hiện các đợt Random Restart
    for _ in range(restarts):
        # Khởi tạo khóa ngẫu nhiên
        current_key_chars = list(ALPHABET_25)
        random.shuffle(current_key_chars)
        current_key = "".join(current_key_chars)

        current_plain = decrypt(cleaned_cipher, current_key)
        current_score = score_key(current_plain, bigram_table)

        best_restart_score = current_score
        best_restart_key = current_key
        best_restart_plain = current_plain

        # Vòng lặp Luyện kim Mô phỏng (Simulated Annealing)
        for step_i in range(1, iterations + 1):
            # Tính nhiệt độ giảm dần theo thời gian
            temp = temp_start * ((temp_end / temp_start) ** (step_i / iterations))

            neighbor_key = _mutate_key(current_key)
            neighbor_plain = decrypt(cleaned_cipher, neighbor_key)
            neighbor_score = score_key(neighbor_plain, bigram_table)

            delta = neighbor_score - current_score

            # Chấp nhận bước chuyển nếu tốt hơn, hoặc kém hơn với xác suất p = exp(delta / temp)
            if delta > 0 or math.exp(delta / temp) > random.random():
                current_score = neighbor_score
                current_key = neighbor_key
                current_plain = neighbor_plain

                # Theo dõi trạng thái tốt nhất trong đợt restart này
                if current_score > best_restart_score:
                    best_restart_score = current_score
                    best_restart_key = current_key
                    best_restart_plain = current_plain

        # Cập nhật kết quả tốt nhất toàn cục
        if best_restart_score > best_global_score:
            best_global_score = best_restart_score
            best_global_key = best_restart_key
            best_global_plaintext = best_restart_plain

    return best_global_plaintext, best_global_key

