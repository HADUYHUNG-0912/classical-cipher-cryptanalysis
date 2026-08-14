"""
experiments/eval_iterations_length.py
======================================
Thử nghiệm đánh giá tương quan giữa:
- Độ dài văn bản L: [100, 200, 500, 1000]
- Số vòng lặp iterations: [1000, 3000, 5000, 10000, 20000]
- Tỷ lệ giải mã đúng (%) và Thời gian xử lý (s) trong thám mã Playfair Cipher.

Tối ưu song song bằng multiprocessing để tính toán nhanh chóng.
Kết quả lưu tại: experiments/results/iterations_length_results.csv
"""

import sys
import time
import random
import string
import csv
from pathlib import Path
from multiprocessing import Pool, cpu_count

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from playfair.cipher import encrypt as playfair_encrypt
from playfair.attack import break_playfair

# ----------------------------------------------------------------
# Cấu hình thử nghiệm
# ----------------------------------------------------------------
TEXT_LENGTHS = [100, 200, 500, 1000]
ITERATION_LIST = [1000, 3000, 5000, 10000, 20000]
N_REPEATS = 5       # Số lần thử nghiệm lặp lại để lấy trung bình
N_RESTARTS = 5      # Số lần random restart cho Playfair attack
RESULTS_DIR = PROJECT_ROOT / "experiments" / "results"

_ENGLISH_SAMPLE = (
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "THISISASAMPLEENGLISHPLAINTEXTFORENCRYPTIONANDCRYPTANALYSISTESTING"
    "INTHEFIELDOFCRYPTOGRAPHYCLASSICALCIPHERSWEREUSEDTOSECUREMESSAGES"
    "BEFOREMODERNCOMPUTERSCAMEINTOPICTURETHEYARENOWCONSIDEREDINSECURE"
    "CRYPTANALYSISISTHESTUDYOFANALYZINGINFORMATIONSYSTEMSINORDERTO"
    "STUDYTHEHIDDENASPECTSOFTHE SYSTEMSCRYPTANALYSISISUSEDTOBREACH"
    "CRYPTOGRAPHICSORTSECURITYSYSTEMSANDGAINESSACCESSTOTHECONTENTSOF"
    "ENCRYPTEDMESSAGESEVENIFTHECRYPTOGRAPHICALKEYISUNKNOWN"
)


def _generate_plaintext(length: int, seed: int) -> str:
    """Sinh văn bản giả lập tiếng Anh chuẩn độ dài `length` (chỉ gồm ký tự A-Z)."""
    rng = random.Random(seed)
    multiplier = (length // len(_ENGLISH_SAMPLE)) + 2
    pool = (_ENGLISH_SAMPLE * multiplier)[: length * 2]
    letters = [c for c in pool if c.isalpha()]
    rng.shuffle(letters)
    return "".join(letters[:length]).upper()


def _random_alpha_key(seed: int, length: int = 8) -> str:
    """Sinh khóa ngẫu nhiên gồm các chữ cái hoa."""
    rng = random.Random(seed + 9999)
    return "".join(rng.choices(string.ascii_uppercase, k=length))


def _accuracy(original: str, recovered: str) -> float:
    """Tính tỉ lệ khớp ký tự giữa văn bản gốc và văn bản thám mã (thang điểm 0.0 -> 1.0)."""
    orig_clean = [c for c in original.upper() if c.isalpha()]
    recv_clean = [c for c in recovered.upper() if c.isalpha()]
    if not orig_clean:
        return 0.0
    compared = min(len(orig_clean), len(recv_clean))
    correct = sum(1 for a, b in zip(orig_clean[:compared], recv_clean[:compared]) if a == b)
    return correct / len(orig_clean)


def _eval_single_config(args):
    L, iters, restarts, n_repeats = args
    accuracies = []
    runtimes = []

    for rep in range(n_repeats):
        seed_val = (L * 10000) + (iters * 10) + rep
        plaintext = _generate_plaintext(L, seed_val)
        key = _random_alpha_key(seed_val, 8)
        ciphertext = playfair_encrypt(plaintext, key)

        t0 = time.perf_counter()
        recovered_plain, _ = break_playfair(
            ciphertext,
            iterations=iters,
            restarts=restarts
        )
        elapsed = time.perf_counter() - t0

        acc = _accuracy(plaintext, recovered_plain) * 100.0
        accuracies.append(acc)
        runtimes.append(elapsed)

    avg_acc = sum(accuracies) / n_repeats
    max_acc = max(accuracies)
    min_acc = min(accuracies)
    avg_time = sum(runtimes) / n_repeats

    return [
        L,
        iters,
        restarts,
        n_repeats,
        round(avg_acc, 2),
        round(max_acc, 2),
        round(min_acc, 2),
        round(avg_time, 3)
    ]


def run_experiment():
    print("=" * 75, flush=True)
    print("  THỬ NGHIỆM ĐÁNH GIÁ TƯƠNG QUAN L vs ITERATIONS vs ĐỘ CHÍNH XÁC (PLAYFAIR)", flush=True)
    print("=" * 75, flush=True)
    print(f"  Độ dài văn bản L     : {TEXT_LENGTHS}", flush=True)
    print(f"  Số vòng lặp          : {ITERATION_LIST}", flush=True)
    print(f"  Số lần lặp lại       : {N_REPEATS} lần/cấu hình", flush=True)
    print(f"  Số lần Random Restart: {N_RESTARTS}", flush=True)
    print(f"  Số luồng CPU xử lý   : {cpu_count()}", flush=True)
    print("-" * 75, flush=True)

    headers = [
        "Do_dai_L",
        "Iterations",
        "Restarts",
        "Repeats",
        "TB_Ti_le_dung_pct",
        "Max_Ti_le_dung_pct",
        "Min_Ti_le_dung_pct",
        "TB_Thoi_gian_s"
    ]

    col_widths = [10, 12, 10, 10, 20, 20, 20, 16]
    row_fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)

    print(row_fmt.format(*headers), flush=True)
    print("  " + "-" * 115, flush=True)

    tasks = [(L, iters, N_RESTARTS, N_REPEATS) for L in TEXT_LENGTHS for iters in ITERATION_LIST]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = RESULTS_DIR / "iterations_length_results.csv"

    all_results = []
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        f.flush()

        with Pool(processes=cpu_count()) as pool:
            for row_data in pool.imap(_eval_single_config, tasks):
                writer.writerow(row_data)
                f.flush()
                all_results.append(row_data)

                L, iters, restarts, n_repeats, avg_acc, max_acc, min_acc, avg_time = row_data
                print(row_fmt.format(
                    L,
                    iters,
                    restarts,
                    n_repeats,
                    f"{avg_acc:.2f}%",
                    f"{max_acc:.2f}%",
                    f"{min_acc:.2f}%",
                    f"{avg_time:.3f}s"
                ), flush=True)

    print("-" * 75, flush=True)
    print(f"  [Đã hoàn tất & xuất dữ liệu kết quả -> {out_csv}]", flush=True)
    print("=" * 75, flush=True)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    run_experiment()
