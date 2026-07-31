# Cryptanalysis Toolkit — Caesar / Vigenère / Playfair

Phần mềm tự động thám mã (không biết khóa trước) cho 3 hệ mật mã cổ điển.

## Mô tả

Dự án xây dựng các thuật toán phân tích tần suất để tự động phá 3 hệ mật mã cổ điển:

- **Caesar cipher** — Brute-force 25 khóa + chấm điểm chi-squared so với tần suất tiếng Anh chuẩn
- **Vigenère cipher** — Ước lượng độ dài khóa bằng Kasiski Examination / Index of Coincidence, sau đó phá từng cột Caesar
- **Playfair cipher** — Hill-climbing / Simulated Annealing với bảng tần suất bigram tiếng Anh để dò khóa 5×5

## Hướng dẫn chạy

### Chạy trực tiếp (Python)

```bash
pip install -r requirements.txt
python main.py
```

### Chạy bằng Docker

```bash
docker build -t crypto-lab .
docker run -it crypto-lab
```

## Cấu trúc thư mục

```
├── caesar/         # Mã hóa + phá mã Caesar
├── vigenere/       # Mã hóa + phá mã Vigenère
├── playfair/       # Mã hóa + phá mã Playfair
├── utils/          # Hàm dùng chung (frequency, text_utils)
├── data/           # Dữ liệu tần suất tiếng Anh
├── tests/          # Unit tests
└── main.py         # CLI menu chính
```

## Phân công nhóm

| Thành viên | Nhiệm vụ |
|------------|----------|
| Người A | Implement `caesar/cipher.py` + `caesar/attack.py`, viết lý thuyết Caesar trong báo cáo |
| Người B | Implement `vigenere/cipher.py` + `vigenere/attack.py`, viết lý thuyết Vigenère |
| Người C | Implement `playfair/cipher.py` + `playfair/attack.py` (phần khó nhất), viết lý thuyết Playfair |
| Cả 3 | Hoàn thiện `utils/frequency.py` và `utils/text_utils.py` (dùng chung), tạo Pull Request để merge vào `main` |

> **Lưu ý:** Không push thẳng vào `main`. Dùng feature branch và Pull Request để review code.