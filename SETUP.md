# Project Setup Instructions — Cryptanalysis Toolkit (Caesar / Vigenère / Playfair)

> File này dùng cho AI coding agent (Claude Code, Cursor, v.v.) đọc và tự động khởi tạo cấu trúc thư mục + file code khung cho project. Agent hãy thực hiện toàn bộ các bước bên dưới theo đúng thứ tự.

## 1. Mục tiêu project

Xây dựng phần mềm tự động thám mã (không biết khóa trước) cho 3 hệ mật mã cổ điển:
- **Caesar cipher** — brute-force 25 khóa + chấm điểm bằng phân tích tần suất chữ cái (chi-squared test so với tần suất tiếng Anh chuẩn)
- **Vigenère cipher** — ước lượng độ dài khóa bằng Kasiski Examination hoặc Index of Coincidence (IC), sau đó tách thành nhiều bài toán Caesar con để giải từng cột
- **Playfair cipher** — do không có tần suất đơn ký tự rõ ràng (mã theo cặp chữ), dùng hill-climbing / simulated annealing với bảng tần suất bigram tiếng Anh để dò khóa 5x5

Chạy trong môi trường Docker để demo an toàn, cô lập.

## 2. Cấu trúc thư mục cần tạo

```
project-root/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
├── data/
│   ├── english_letter_freq.json      # tần suất đơn ký tự tiếng Anh
│   ├── english_bigram_freq.json      # tần suất bigram tiếng Anh (cho Playfair)
│   └── sample_corpus.txt             # văn bản mẫu để tạo ciphertext test
├── caesar/
│   ├── __init__.py
│   ├── cipher.py                     # hàm encrypt/decrypt Caesar cơ bản
│   └── attack.py                     # thuật toán phá mã Caesar
├── vigenere/
│   ├── __init__.py
│   ├── cipher.py                     # hàm encrypt/decrypt Vigenère cơ bản
│   └── attack.py                     # thuật toán phá mã Vigenère (Kasiski + IC)
├── playfair/
│   ├── __init__.py
│   ├── cipher.py                     # hàm encrypt/decrypt Playfair cơ bản
│   └── attack.py                     # thuật toán phá mã Playfair (hill-climbing)
├── utils/
│   ├── __init__.py
│   ├── frequency.py                  # hàm dùng chung: tính tần suất, chi-squared, IC
│   └── text_utils.py                 # hàm dùng chung: chuẩn hóa văn bản, đọc/ghi file
├── tests/
│   ├── test_caesar.py
│   ├── test_vigenere.py
│   └── test_playfair.py
└── main.py                           # menu CLI chọn Caesar / Vigenère / Playfair
```

## 3. Nội dung khung từng file (agent tạo file với nội dung stub bên dưới, KHÔNG cần implement thuật toán đầy đủ — chỉ tạo hàm rỗng có docstring và TODO để từng thành viên nhóm tự điền)

### `requirements.txt`
```
numpy
```
(Không cần thư viện crypto ngoài — mục đích môn học là tự viết thuật toán.)

### `Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### `.gitignore`
```
__pycache__/
*.pyc
.venv/
venv/
.DS_Store
.env
```

### `data/english_letter_freq.json`
Tạo JSON với tần suất 26 chữ cái tiếng Anh chuẩn (nguồn: thống kê ngôn ngữ học phổ biến), dạng:
```json
{"A": 8.17, "B": 1.49, "C": 2.78, "...": "..."}
```
(Agent điền đủ 26 chữ cái với giá trị tần suất % chuẩn được biết rộng rãi.)

### `data/english_bigram_freq.json`
Stub file, để trống dict `{}` kèm comment TODO: cần điền bảng tần suất bigram tiếng Anh (dùng cho Playfair attack).

### `data/sample_corpus.txt`
Stub: 1-2 đoạn văn tiếng Anh ngắn mẫu (public domain) để làm dữ liệu test tạo ciphertext.

### `utils/text_utils.py`
```python
"""Các hàm tiện ích xử lý văn bản dùng chung cho cả 3 module."""

def clean_text(text: str) -> str:
    """Chuẩn hóa văn bản: viết hoa toàn bộ, chỉ giữ lại chữ cái A-Z."""
    # TODO: implement
    pass

def read_file(path: str) -> str:
    """Đọc nội dung file văn bản."""
    # TODO: implement
    pass

def write_file(path: str, content: str) -> None:
    """Ghi nội dung ra file."""
    # TODO: implement
    pass
```

### `utils/frequency.py`
```python
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
```

### `caesar/cipher.py`
```python
"""Mã hóa/giải mã Caesar cipher cơ bản (dùng để tạo ciphertext test)."""

def encrypt(plaintext: str, shift: int) -> str:
    # TODO: implement
    pass

def decrypt(ciphertext: str, shift: int) -> str:
    # TODO: implement
    pass
```

### `caesar/attack.py`
```python
"""Thuật toán tự động phá mã Caesar — brute-force 25 khóa + chấm điểm chi-squared."""
from utils.frequency import letter_frequency, chi_squared_score
from utils.text_utils import clean_text

def break_caesar(ciphertext: str) -> tuple[str, int]:
    """Thử tất cả 25 khóa dịch, trả về (plaintext, key) có chi-squared thấp nhất.
    TODO (người phụ trách Caesar implement):
    1. Với mỗi shift từ 0-25, decrypt thử
    2. Tính chi-squared so với tần suất tiếng Anh chuẩn
    3. Trả về kết quả có điểm thấp nhất (giống tiếng Anh nhất)
    """
    pass
```

### `vigenere/cipher.py`
```python
"""Mã hóa/giải mã Vigenère cipher cơ bản."""

def encrypt(plaintext: str, key: str) -> str:
    # TODO: implement
    pass

def decrypt(ciphertext: str, key: str) -> str:
    # TODO: implement
    pass
```

### `vigenere/attack.py`
```python
"""Thuật toán tự động phá mã Vigenère — ước lượng độ dài khóa (Kasiski/IC) 
rồi tách thành nhiều Caesar con để giải."""
from utils.frequency import index_of_coincidence

def estimate_key_length(ciphertext: str, max_len: int = 20) -> int:
    """TODO (người phụ trách Vigenère implement):
    Dùng Kasiski Examination hoặc Index of Coincidence để đoán độ dài khóa."""
    pass

def break_vigenere(ciphertext: str) -> tuple[str, str]:
    """TODO:
    1. Gọi estimate_key_length()
    2. Tách ciphertext thành N nhóm ký tự theo vị trí % key_length
    3. Áp dụng thuật toán phá Caesar cho từng nhóm để tìm từng ký tự khóa
    4. Ghép khóa lại, giải mã toàn bộ văn bản
    Trả về (plaintext, key)
    """
    pass
```

### `playfair/cipher.py`
```python
"""Mã hóa/giải mã Playfair cipher cơ bản (bảng 5x5)."""

def generate_key_square(key: str) -> list:
    # TODO: implement — tạo bảng 5x5 từ khóa (I/J gộp chung)
    pass

def encrypt(plaintext: str, key: str) -> str:
    # TODO: implement
    pass

def decrypt(ciphertext: str, key: str) -> str:
    # TODO: implement
    pass
```

### `playfair/attack.py`
```python
"""Thuật toán tự động phá mã Playfair — hill-climbing dùng tần suất bigram
(khó nhất trong 3 hệ, không có phân tích tần suất đơn giản)."""
from utils.frequency import chi_squared_score

def score_key(plaintext_guess: str, bigram_freq_table: dict) -> float:
    """TODO: chấm điểm 1 bảng khóa dựa trên độ khớp bigram với tiếng Anh chuẩn."""
    pass

def break_playfair(ciphertext: str, iterations: int = 5000) -> tuple[str, str]:
    """TODO (người phụ trách Playfair implement — phần khó nhất):
    1. Khởi tạo 1 bảng khóa 5x5 ngẫu nhiên
    2. Lặp: hoán đổi ngẫu nhiên 2 ký tự trong bảng, decrypt thử, chấm điểm bigram
    3. Nếu điểm tốt hơn thì giữ, nếu không thì giữ nguyên (hill-climbing)
    4. Lặp lại nhiều lần khởi tạo (random restart) để tránh local optimum
    Trả về (plaintext, key_square_as_string)
    """
    pass
```

### `main.py`
```python
"""CLI menu chính — chọn hệ mật mã để phá."""
from caesar.attack import break_caesar
from vigenere.attack import break_vigenere
from playfair.attack import break_playfair

def main():
    print("=== Cryptanalysis Toolkit ===")
    print("1. Caesar cipher")
    print("2. Vigenère cipher")
    print("3. Playfair cipher")
    choice = input("Chọn hệ mật mã cần phá (1-3): ")

    ciphertext = input("Nhập ciphertext: ")

    if choice == "1":
        plaintext, key = break_caesar(ciphertext)
    elif choice == "2":
        plaintext, key = break_vigenere(ciphertext)
    elif choice == "3":
        plaintext, key = break_playfair(ciphertext)
    else:
        print("Lựa chọn không hợp lệ.")
        return

    print(f"\nKhóa tìm được: {key}")
    print(f"Plaintext: {plaintext}")

if __name__ == "__main__":
    main()
```

### `tests/test_caesar.py`, `test_vigenere.py`, `test_playfair.py`
Mỗi file tạo 1 test stub đơn giản dùng `assert`, ví dụ:
```python
"""Test cơ bản cho module Caesar. TODO: bổ sung test case sau khi implement attack.py"""
from caesar.cipher import encrypt, decrypt

def test_encrypt_decrypt_roundtrip():
    # TODO: viết test sau khi cipher.py được implement
    pass
```

### `README.md`
Tạo README ngắn gồm:
- Tên project
- Mô tả (thám mã 3 hệ mật cổ điển bằng phân tích tần suất)
- Hướng dẫn chạy: `pip install -r requirements.txt` rồi `python main.py`, hoặc `docker build -t crypto-lab .` rồi `docker run -it crypto-lab`
- Phân công: Người A - Caesar, Người B - Vigenère, Người C - Playfair

## 4. Lệnh git để agent chạy sau khi tạo xong cấu trúc

```bash
git init
git add .
git commit -m "Init project structure: Caesar/Vigenère/Playfair cryptanalysis toolkit"
git branch -M main
git remote add origin <URL_REPO_GITHUB_CUA_NHOM>
git push -u origin main
```

> Lưu ý: agent cần thay `<URL_REPO_GITHUB_CUA_NHOM>` bằng URL repo thật do nhóm cung cấp trước khi chạy lệnh push.

## 5. Sau khi setup xong, phân công tiếp theo cho 3 thành viên

- **Người A:** implement `caesar/cipher.py` + `caesar/attack.py`, viết phần lý thuyết Caesar trong báo cáo
- **Người B:** implement `vigenere/cipher.py` + `vigenere/attack.py`, viết phần lý thuyết Vigenère
- **Người C:** implement `playfair/cipher.py` + `playfair/attack.py` (phần khó nhất), viết phần lý thuyết Playfair
- Cả 3 cùng hoàn thiện `utils/frequency.py` và `utils/text_utils.py` (dùng chung), rồi tạo Pull Request để merge vào `main`, tránh push thẳng.
