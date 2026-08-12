"""
experiments/benchmark.py
========================
Framework thuc nghiem dung chung cho ca ba he mat ma: Caesar, Vigenere, Playfair.

Cach dung:
    python -m experiments.benchmark              # chay tat ca
    python -m experiments.benchmark caesar       # chi Caesar
    python -m experiments.benchmark vigenere     # chi Vigenere
    python -m experiments.benchmark playfair     # chi Playfair

Ket qua duoc in ra bang tren console va luu vao experiments/results/<cipher>_results.csv
"""

import sys
import time
import random
import string
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from caesar.cipher import encrypt as caesar_encrypt
from caesar.attack import break_caesar
from vigenere.cipher import encrypt as vigenere_encrypt
from vigenere.attack import break_vigenere
from playfair.cipher import encrypt as playfair_encrypt
from playfair.attack import break_playfair

# ----------------------------------------------------------------
# Cau hinh thuc nghiem
# ----------------------------------------------------------------
TEXT_LENGTHS = [50, 100, 500, 1000]
N_REPEATS = 5
VIGENERE_KEY_LENGTHS = [2, 4, 6, 8, 10]
PLAYFAIR_ITERATIONS = 3000
PLAYFAIR_RESTARTS = 10
RESULTS_DIR = PROJECT_ROOT / "experiments" / "results"

# ----------------------------------------------------------------
# Tien ich
# ----------------------------------------------------------------
_ENGLISH_SAMPLE = (
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "THISISASAMPLEENGLISHPLAINTEXTFORENCRYPTIONANDCRYPTANALYSISTESTING"
    "INTHEFIELDOFCRYPTOGRAPHYCLASSICALCIPHERSWEREUSEDTOSECUREMESSAGES"
    "BEFOREMODERNCOMPUTERSCAMEINTOPICTURETHEYARENOWCONSIDEREDINSECURE"
)


def _generate_plaintext(length: int) -> str:
    """Sinh van ban tieng Anh gia lap (chi gom chu cai hoa) du `length` ky tu."""
    multiplier = (length // len(_ENGLISH_SAMPLE)) + 2
    pool = (_ENGLISH_SAMPLE * multiplier)[: length * 2]
    letters = [c for c in pool if c.isalpha()]
    random.shuffle(letters)
    return "".join(letters[:length]).upper()


def _random_alpha_key(length: int) -> str:
    """Sinh khoa ngau nhien gom `length` chu cai hoa."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


def _accuracy(original: str, recovered: str) -> float:
    """Tinh ti le ky tu dung (chi dem chu cai)."""
    orig_clean = [c for c in original.upper() if c.isalpha()]
    recv_clean = [c for c in recovered.upper() if c.isalpha()]
    if not orig_clean:
        return 0.0
    compared = min(len(orig_clean), len(recv_clean))
    correct = sum(1 for a, b in zip(orig_clean[:compared], recv_clean[:compared]) if a == b)
    return correct / len(orig_clean)


def _print_header(title: str):
    print()
    print("=" * 65)
    print("  " + title)
    print("=" * 65)


def _print_row(cols, widths):
    row = "  ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(row)


def _save_csv(filename: str, headers: list, rows: list):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RESULTS_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("\n  [Da luu ket qua -> " + str(filepath) + "]")


# ----------------------------------------------------------------
# CAESAR BENCHMARK
# ----------------------------------------------------------------
def run_caesar_benchmark():
    _print_header("CAESAR CIPHER -- Ket qua thuc nghiem")
    headers = ["Do dai L", "Lap N", "TB thoi gian (ms)", "Ti le pha dung (%)"]
    widths = [12, 8, 20, 22]
    _print_row(headers, widths)
    print("  " + "-" * 60)
    all_rows = []
    for L in TEXT_LENGTHS:
        times_ms, success_rates = [], []
        for _ in range(N_REPEATS):
            plaintext = _generate_plaintext(L)
            true_key = random.randint(1, 25)
            ciphertext = caesar_encrypt(plaintext, true_key)
            t0 = time.perf_counter()
            recovered_plain, recovered_key = break_caesar(ciphertext)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            times_ms.append(elapsed_ms)
            key_correct = recovered_key == true_key
            acc = _accuracy(plaintext, recovered_plain)
            success_rates.append(1.0 if key_correct else acc)
        avg_time = sum(times_ms) / N_REPEATS
        avg_success = (sum(success_rates) / N_REPEATS) * 100
        _print_row([L, N_REPEATS, "{:.2f}".format(avg_time), "{:.1f}".format(avg_success)], widths)
        all_rows.append([L, N_REPEATS, round(avg_time, 2), round(avg_success, 1)])
    _save_csv("caesar_results.csv", headers, all_rows)


# ----------------------------------------------------------------
# VIGENERE BENCHMARK
# ----------------------------------------------------------------
def run_vigenere_benchmark():
    _print_header("VIGENERE CIPHER -- Ket qua thuc nghiem")
    headers = ["Do dai L", "Key len", "Lap N", "TB thoi gian (ms)", "Ti le pha dung (%)"]
    widths = [12, 9, 8, 20, 22]
    _print_row(headers, widths)
    print("  " + "-" * 68)
    all_rows = []
    for L in TEXT_LENGTHS:
        for kl in VIGENERE_KEY_LENGTHS:
            times_ms, success_rates = [], []
            for _ in range(N_REPEATS):
                plaintext = _generate_plaintext(L)
                true_key = _random_alpha_key(kl)
                ciphertext = vigenere_encrypt(plaintext, true_key)
                t0 = time.perf_counter()
                recovered_plain, _ = break_vigenere(ciphertext)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                times_ms.append(elapsed_ms)
                success_rates.append(_accuracy(plaintext, recovered_plain))
            avg_time = sum(times_ms) / N_REPEATS
            avg_success = (sum(success_rates) / N_REPEATS) * 100
            _print_row(
                [L, kl, N_REPEATS, "{:.2f}".format(avg_time), "{:.1f}".format(avg_success)],
                widths,
            )
            all_rows.append([L, kl, N_REPEATS, round(avg_time, 2), round(avg_success, 1)])
    _save_csv("vigenere_results.csv", headers, all_rows)


# ----------------------------------------------------------------
# PLAYFAIR BENCHMARK
# ----------------------------------------------------------------
def run_playfair_benchmark():
    _print_header("PLAYFAIR CIPHER -- Ket qua thuc nghiem")
    print("  (iterations=" + str(PLAYFAIR_ITERATIONS) + ", restarts=" + str(PLAYFAIR_RESTARTS) + ")")
    headers = ["Do dai L", "Lap N", "TB thoi gian (ms)", "TB do chinh xac (%)"]
    widths = [12, 8, 20, 22]
    _print_row(headers, widths)
    print("  " + "-" * 60)
    all_rows = []
    for L in TEXT_LENGTHS:
        times_ms, accuracies = [], []
        for _ in range(N_REPEATS):
            plaintext = _generate_plaintext(L)
            true_key = _random_alpha_key(8)
            ciphertext = playfair_encrypt(plaintext, true_key)
            t0 = time.perf_counter()
            recovered_plain, _ = break_playfair(
                ciphertext,
                iterations=PLAYFAIR_ITERATIONS,
                restarts=PLAYFAIR_RESTARTS,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
            times_ms.append(elapsed_ms)
            accuracies.append(_accuracy(plaintext, recovered_plain))
        avg_time = sum(times_ms) / N_REPEATS
        avg_acc = (sum(accuracies) / N_REPEATS) * 100
        _print_row([L, N_REPEATS, "{:.0f}".format(avg_time), "{:.1f}".format(avg_acc)], widths)
        all_rows.append([L, N_REPEATS, round(avg_time, 0), round(avg_acc, 1)])
    _save_csv("playfair_results.csv", headers, all_rows)


# ----------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    print()
    print("===== CRYPTANALYSIS BENCHMARK FRAMEWORK v1.0 =====")
    print("  Che do   : " + target.upper())
    print("  Lap lai  : " + str(N_REPEATS) + " lan/cau hinh")
    print("  Do dai L : " + str(TEXT_LENGTHS))

    if target in ("all", "caesar"):
        run_caesar_benchmark()

    if target in ("all", "vigenere"):
        run_vigenere_benchmark()

    if target in ("all", "playfair"):
        run_playfair_benchmark()

    print()
    print("Hoan tat! Xem ket qua tai: experiments/results/")


if __name__ == "__main__":
    main()
