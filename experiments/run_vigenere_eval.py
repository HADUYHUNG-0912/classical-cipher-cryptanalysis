"""
experiments/run_vigenere_eval.py
================================
Đánh giá chi tiết thuật toán phá mã Vigenère:
1. Độ chính xác của ước lượng độ dài khóa bằng Index of Coincidence (IC).
2. Tỉ lệ phá khóa thành công hoàn toàn (Đúng 100% key).
3. Độ chính xác ký tự giải mã (Plaintext Accuracy %).

Tham số:
- Độ dài key: 2 đến 10
- Chiều dài văn bản L: 50, 100, 500, 1000
- Số lần thử nghiệm N: 20 lần cho mỗi cấu hình (tổng cộng 9 * 4 * 20 = 720 lượt thử)
"""

import sys
import time
import random
import string
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from vigenere.cipher import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from vigenere.attack import estimate_key_length, break_vigenere
from utils.frequency import index_of_coincidence

# Corpus tiếng Anh tự nhiên mẫu để trích xuất đoạn văn bản liên tục
CORPUS = """
IT IS A TRUTH UNIVERSALLY ACKNOWLEDGED THAT A SINGLE MAN IN POSSESSION OF A GOOD FORTUNE MUST BE IN WANT OF A WIFE
HOWEVER LITTLE KNOWN THE FEELINGS OR VIEWS OF SUCH A MAN MAY BE ON HIS FIRST ENTERING A NEIGHBORHOOD THIS TRUTH IS SO WELL FIXED IN THE MINDS OF THE SURROUNDING FAMILIES THAT HE IS CONSIDERED THE RIGHTFUL PROPERTY OF SOME ONE OR OTHER OF THEIR DAUGHTERS
MY DEAR MR BENNET SAID HIS LADY TO HIM ONE DAY HAVE YOU HEARD THAT NETHERFIELD PARK IS LET AT LAST
MR BENNET REPLIED THAT HE HAD NOT
BUT IT IS RETURNED SHE FOR MRS LONG HAS JUST BEEN HERE AND SHE TOLD ME ALL ABOUT IT
MR BENNET MADE NO ANSWER
DO YOU NOT WANT TO KNOW WHO HAS TAKEN IT CRIED HIS WIFE IMPATIENTLY
YOU WANT TO TELL ME AND I HAVE NO OBJECTION TO HEARING IT
THIS WAS INVITATION ENOUGH
WHY MY DEAR YOU MUST KNOW MRS LONG SAYS THAT NETHERFIELD IS TAKEN BY A YOUNG MAN OF LARGE FORTUNE FROM THE NORTH OF ENGLAND THAT HE CAME DOWN ON MONDAY IN A CHAISE AND FOUR TO SEE THE PLACE AND WAS SO MUCH DELIGHTED WITH IT THAT HE AGREED WITH MR MORRIS IMMEDIATELY THAT HE IS TO TAKE POSSESSION BEFORE MICHAELMAS AND SOME OF HIS SERVANTS ARE TO BE IN THE HOUSE BY THE END OF NEXT WEEK
WHAT IS HIS NAME
BINGLEY
IS HE MARRIED OR SINGLE
OH SINGLE MY DEAR TO BE SURE A SINGLE MAN OF LARGE FORTUNE FOUR OR FIVE THOUSAND A YEAR WHAT A FINE THING FOR OUR GIRLS
HOW SO HOW CAN IT AFFECT THEM
MY DEAR MR BENNET REPLIED HIS WIFE HOW CAN YOU BE SO TIRESOME YOU MUST KNOW THAT I AM THINKING OF HIS MARRIAGE WITH ONE OF THEM
IS THAT HIS DESIGN IN SETTLING HERE
DESIGN NONSENSE HOW CAN YOU TALK SO BUT IT IS VERY LIKELY THAT HE MAY FALL IN LOVE WITH ONE OF THEM AND THEREFORE YOU MUST VISIT HIM AS SOON AS HE COMES
I SEE NO OCCASION FOR THAT YOU AND THE GIRLS MAY GO OR YOU MAY SEND THEM BY THEMSELVES WHICH PERHAPS WILL BE STILL BETTER FOR AS YOU ARE AS HANDSOME AS ANY OF THEM MR BINGLEY MAY LIKE YOU THE BEST OF THE PARTY
MY DEAR YOU FLATTER ME I CERTAINLY HAVE HAD MY SHARE OF BEAUTY BUT I DO NOT PRETEND TO BE ANYTHING EXTRAORDINARY NOW WHEN A WOMAN HAS FIVE GROWN UP DAUGHTERS SHE OUGHT TO GIVE OVER THINKING OF HER OWN BEAUTY
IN SUCH CASES IT IS A COMMON THING FOR A WOMAN NOT TO HAVE MUCH BEAUTY TO THINK OF
BUT MY DEAR YOU MUST INDEED GO AND SEE MR BINGLEY WHEN HE COMES INTO THE NEIGHBORHOOD
IT IS MORE THAN I ENGAGE FOR I ASSURE YOU
BUT CONSIDER YOUR DAUGHTERS ONLY THINK WHAT AN ESTABLISHMENT IT WOULD BE FOR ONE OF THEM SIR WILLIAM AND LADY LUCAS ARE DETERMINED TO GO MERELY ON THAT ACCOUNT FOR IN GENERAL YOU KNOW THEY VISIT NO NEWCOMERS INDEED YOU MUST GO FOR IT WILL BE IMPOSSIBLE FOR US TO VISIT HIM IF YOU DO NOT
YOU ARE OVER SCRUPULOUS SURELY I DARE SAY MR BINGLEY WILL BE VERY GLAD TO SEE YOU AND I WILL SEND A FEW LINES BY YOU TO ASSURE HIM OF MY HEARTY CONSENT TO HIS MARRYING WHICH EVER HE CHOOSES OF THE GIRLS THOUGH I MUST THROW IN A GOOD WORD FOR MY LITTLE LIZZY
I DESIRE YOU WILL DO NO SUCH THING LIZZY IS NOT A BIT BETTER THAN THE OTHERS AND I AM SURE SHE IS NOT HALF SO HANDSOME AS JANE NOR HALF SO GOOD HUMORED AS LYDIA BUT YOU ARE ALWAYS GIVING HER THE PREFERENCE
THEY HAVE NONE OF THEM MUCH TO RECOMMEND THEM REPLIED HE THEY ARE ALL SILLY AND IGNORANT LIKE OTHER GIRLS BUT LIZZY HAS SOMETHING MORE OF QUICKNESS THAN HER SISTERS
MR BENNET HOW CAN YOU ABUSE YOUR OWN CHILDREN IN SUCH A WAY YOU TAKE DELIGHT IN VEXING ME YOU HAVE NO COMPASSION FOR MY POOR NERVES
YOU MISTAKE ME MY DEAR I HAVE THE HIGHEST RESPECT FOR YOUR NERVES THEY ARE MY OLD FRIENDS I HAVE HEARD YOU MENTION THEM WITH CONSIDERATION THESE LAST TWENTY YEARS AT LEAST
AH YOU DO NOT KNOW WHAT I SUFFER
BUT I HOPE YOU WILL GET OVER IT AND LIVE TO SEE MANY YOUNG MEN OF FOUR THOUSAND A YEAR COME INTO THE NEIGHBORHOOD
IT WILL BE NO USE TO US IF TWENTY SUCH SHOULD COME SINCE YOU WILL NOT VISIT THEM
DEPEND UPON IT MY DEAR THAT WHEN THERE ARE TWENTY I WILL VISIT THEM ALL
MR BENNET WAS SO ODD A MIXTURE OF QUICK PARTS SARCASTIC HUMOR RESERVE AND CAPRICE THAT THE EXPERIENCE OF THREE AND TWENTY YEARS HAD BEEN INSUFFICIENT TO MAKE HIS WIFE UNDERSTAND HIS CHARACTER HER MIND WAS LESS DIFFICULT TO DEVELOP SHE WAS A WOMAN OF MEAN UNDERSTANDING LITTLE INFORMATION AND UNCERTAIN TEMPER WHEN SHE WAS DISCONTENTED SHE FANCY HERSELF NERVOUS THE BUSINESS OF HER LIFE WAS TO GET HER DAUGHTERS MARRIED ITS SOLACE WAS VISITING AND NEWS
"""

# Làm sạch corpus chỉ giữ A-Z
CLEAN_CORPUS = "".join(c for c in CORPUS.upper() if c.isalpha())


def get_random_plaintext(length: int) -> str:
    """Trích xuất một đoạn văn bản tiếng Anh tự nhiên liên tục dài `length` từ CORPUS."""
    max_start = len(CLEAN_CORPUS) - length
    if max_start <= 0:
        # Nếu corpus ngắn hơn length, lặp lại corpus
        repeated = CLEAN_CORPUS * ((length // len(CLEAN_CORPUS)) + 2)
        start = random.randint(0, len(CLEAN_CORPUS) - 1)
        return repeated[start : start + length]
    start = random.randint(0, max_start)
    return CLEAN_CORPUS[start : start + length]


def random_key(length: int) -> str:
    """Sinh khóa ngẫu nhiên gồm `length` chữ cái hoa."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


def accuracy(orig: str, rec: str) -> float:
    """Tính tỉ lệ % chữ cái giải mã đúng."""
    if not orig:
        return 0.0
    correct = sum(1 for a, b in zip(orig, rec) if a == b)
    return correct / len(orig)


def run_experiment(n_repeats: int = 20):
    key_lengths = list(range(2, 11))  # 2 to 10
    text_lengths = [50, 100, 500, 1000]

    print("=" * 85)
    print("  KẾT QUẢ THỰC NGHIỆM PHÁ MÃ VIGENÈRE & ƯỚC LƯỢNG ĐỘ DÀI KHÓA BẰNG IC")
    print(f"  Số lần thử nghiệm mỗi cấu hình: N = {n_repeats}")
    print("=" * 85)

    headers = [
        "Độ dài L",
        "Key Len",
        "IC Đúng (%)",
        "Phá Key Đúng (%)",
        "Độ chính xác VB (%)",
        "Thời gian (ms)",
    ]
    widths = [10, 10, 15, 18, 20, 15]

    row_fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(row_fmt.format(*headers))
    print("-" * 92)

    results_data = []

    for L in text_lengths:
        for kl in key_lengths:
            ic_correct = 0
            key_correct = 0
            acc_list = []
            time_list = []

            for _ in range(n_repeats):
                plaintext = get_random_plaintext(L)
                true_key = random_key(kl)
                ciphertext = vigenere_encrypt(plaintext, true_key)

                t0 = time.perf_counter()
                est_kl = estimate_key_length(ciphertext)
                rec_plain, rec_key = break_vigenere(ciphertext)
                elapsed_ms = (time.perf_counter() - t0) * 1000

                time_list.append(elapsed_ms)

                if est_kl == kl:
                    ic_correct += 1
                if rec_key == true_key:
                    key_correct += 1

                acc_list.append(accuracy(plaintext, rec_plain))

            ic_acc_pct = (ic_correct / n_repeats) * 100
            key_acc_pct = (key_correct / n_repeats) * 100
            text_acc_pct = (sum(acc_list) / n_repeats) * 100
            avg_time = sum(time_list) / n_repeats

            print(
                row_fmt.format(
                    L,
                    kl,
                    f"{ic_acc_pct:.1f}%",
                    f"{key_acc_pct:.1f}%",
                    f"{text_acc_pct:.1f}%",
                    f"{avg_time:.2f}",
                )
            )

            results_data.append(
                {
                    "Text_Length": L,
                    "Key_Length": kl,
                    "IC_Accuracy_Pct": round(ic_acc_pct, 1),
                    "Key_Recovery_Pct": round(key_acc_pct, 1),
                    "Text_Accuracy_Pct": round(text_acc_pct, 1),
                    "Avg_Time_Ms": round(avg_time, 2),
                }
            )

    # Lưu kết quả ra file CSV
    out_dir = PROJECT_ROOT / "experiments" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "vigenere_ic_detailed_results.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results_data[0].keys())
        writer.writeheader()
        writer.writerows(results_data)

    print("\n  [Đã lưu kết quả chi tiết vào: " + str(csv_path) + "]")
    return results_data


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    run_experiment(n_repeats=25)
