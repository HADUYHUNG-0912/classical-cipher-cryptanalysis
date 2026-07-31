# Checklist Quản Lý Tiến Độ Đồ Án (Cryptanalysis Toolkit)

> File checklist này dùng để theo dõi tiến độ công việc theo từng tuần, cấu trúc báo cáo, slide thuyết trình và điều kiện nộp bài đồ án **Thám mã Mật mã Cổ điển (Caesar / Vigenère / Playfair)**.

---

## 📅 1. Kế hoạch Công việc theo Tuần

### 🔹 Tuần 1: Setup + Code Cơ bản
- [x] Cài đặt Docker, VS Code, tạo GitHub repository và mời 2 thành viên vào repo.
- [x] Chạy Agent setup cấu trúc thư mục & file khung theo [`SETUP.md`](file:///e:/An%20toàn%20TT/project/classical-cipher-cryptanalysis/SETUP.md).
- [ ] **Mã hóa / Giải mã cơ bản (`cipher.py`)**:
  - [ ] **Hưng**: Hoàn thiện `caesar/cipher.py` (`encrypt`/`decrypt`).
  - [ ] **Nguyễn Ánh Duy**: Hoàn thiện `vigenere/cipher.py` (`encrypt`/`decrypt`).
  - [ ] **Minh Hiếu**: Hoàn thiện `playfair/cipher.py` (`generate_key_square`, `encrypt`/`decrypt`).
- [x] **Dữ liệu tần suất**:
  - [x] Đã chuẩn bị `data/english_letter_freq.json` (tần suất chữ cái).
  - [x] Đã điền bảng tần suất bigram `data/english_bigram_freq.json` (top 100 bigrams).
  - [x] Đã chuẩn bị `data/sample_corpus.txt` (văn bản mẫu test).
- [x] **Hàm tiện ích (`utils/`)**:
  - [x] Hoàn thiện `utils/text_utils.py` (`clean_text`, `read_file`, `write_file`).
  - [x] Hoàn thiện `utils/frequency.py` (`letter_frequency`, `chi_squared_score`, `index_of_coincidence`, `bigram_frequency`, `bigram_log_score`).
- [ ] **Thám mã bản đầu tiên (`attack.py`)**:
  - [ ] Viết bản thử nghiệm cho `caesar/attack.py` (chạy được với ciphertext ngắn, sạch).
- [ ] **Deliverable cuối Tuần 1**: 3 module `cipher` hoạt động, ít nhất `caesar/attack.py` chạy được cơ bản.

---

### 🔹 Tuần 2: Hoàn thiện Thuật toán Phá mã + Thực nghiệm
- [ ] **Thuật toán phá mã nâng cao (`attack.py`)**:
  - [ ] **Hưng**: Hoàn thiện `caesar/attack.py` (Brute-force 25 khóa + Chi-squared).
  - [ ] **Nguyễn Ánh Duy**: Hoàn thiện `vigenere/attack.py` (Kasiski / IC đoán key length + giải từng cột Caesar).
  - [ ] **Minh Hiếu**: Hoàn thiện `playfair/attack.py` (Hill-climbing / Simulated Annealing với Random Restart).
- [ ] **Thực nghiệm & Đo đạc chỉ số**:
  - [ ] Test với các độ dài ciphertext khác nhau (ngắn / trung bình / dài) để đo tỷ lệ giải mã đúng.
  - [ ] Test Vigenère với độ dài khóa khác nhau (ngắn / dài), ghi nhận độ chính xác của Kasiski/IC.
  - [ ] Thu thập số liệu, thời gian chạy và vẽ biểu đồ (% thành công, thời gian giải mã).
- [ ] **Đóng gói Docker**:
  - [ ] Đóng gói toàn bộ dự án vào Docker với `Dockerfile`.
  - [ ] Test chạy thành công bằng `docker build -t crypto-lab .` và `docker run -it crypto-lab`.
- [ ] **Deliverable cuối Tuần 2**: Toàn bộ 3 module attack hoạt động ổn định trong Docker, có số liệu thực nghiệm đầy đủ.

---

### 🔹 Tuần 3: Viết Báo cáo
- [ ] **Báo cáo thành phần**:
  - [ ] **Hưng**: Viết phần lý thuyết + kết quả thực nghiệm Caesar vào [`docs/caesar_report.md`](file:///e:/An%20toàn%20TT/project/classical-cipher-cryptanalysis/docs/caesar_report.md).
  - [ ] **Nguyễn Ánh Duy**: Viết phần lý thuyết + kết quả thực nghiệm Vigenère vào [`docs/vigenere_report.md`](file:///e:/An%20toàn%20TT/project/classical-cipher-cryptanalysis/docs/vigenere_report.md).
  - [ ] **Minh Hiếu**: Viết phần lý thuyết + kết quả thực nghiệm Playfair vào [`docs/playfair_report.md`](file:///e:/An%20toàn%20TT/project/classical-cipher-cryptanalysis/docs/playfair_report.md).
- [ ] **Báo cáo chung (Cả nhóm)**:
  - [ ] Viết phần Mục tiêu, Kịch bản thực nghiệm (Lab Docker), và Biện pháp phòng chống.
  - [ ] Tổng hợp ghép thành file báo cáo hoàn chỉnh [`docs/final_report.md`](file:///e:/An%20toàn%20TT/project/classical-cipher-cryptanalysis/docs/final_report.md) theo 5 phần bắt buộc.
- [ ] **Review & Rà soát**:
  - [ ] Review chéo báo cáo giữa 3 thành viên, chỉnh sửa lỗi chính tả, công thức toán và định dạng.
- [ ] **Deliverable cuối Tuần 3**: File Báo cáo hoàn chỉnh bản nháp.

---

### 🔹 Tuần 4: Slide Thuyết trình + Tổng duyệt & Nộp bài
- [ ] **Soạn Slide (Mẫu UTH)**:
  - [ ] Thiết kế 25 - 40 slide theo mẫu UTH (Font size: Tiêu đề 32pt, Nội dung 26pt).
  - [ ] Chia phần soạn slide: Mỗi người phụ trách thuật toán của mình; phần chung chia đều.
- [ ] **Kịch bản Demo & Tập luyện**:
  - [ ] Chuẩn bị kịch bản demo trực tiếp (chạy Docker trước lớp với các ciphertext mẫu).
  - [ ] Chụp/Quay video demo dự phòng đưa vào slide.
  - [ ] Khớp thời gian & tập thuyết trình thử toàn bộ nhóm.
- [ ] **Tổng duyệt lần cuối**:
  - [ ] Kiểm tra lại Code + Báo cáo + Slide + Docker.
- [ ] **Deliverable cuối Tuần 4**: Sản phẩm hoàn chỉnh sẵn sàng demo và nộp bài.

---

## 📑 2. Cấu trúc Báo cáo (5 Phần Bắt buộc)

- [ ] **Phần 1: Mục tiêu**
  - [ ] Mục đích xây dựng công cụ thám mã tự động.
  - [ ] Phạm vi 3 hệ mật (Caesar, Vigenère, Playfair).
  - [ ] Ứng dụng thực tế trong giảng dạy & nghiên cứu An toàn thông tin.
- [ ] **Phần 2: Cơ sở lý thuyết**
  - [ ] Cơ chế mã hóa / giải mã Caesar, Vigenère, Playfair.
  - [ ] Lý thuyết phân tích tần suất chữ cái (Frequency Analysis) & Chi-squared test.
  - [ ] Kasiski Examination / Index of Coincidence (cho Vigenère).
  - [ ] Hill-climbing / Simulated Annealing với Bigram Frequency (cho Playfair).
- [ ] **Phần 3: Kịch bản thực nghiệm**
  - [ ] Mô tả môi trường Lab (Docker container, cấu hình hệ thống).
  - [ ] Bộ dữ liệu test (corpus mẫu, độ dài văn bản, độ dài khóa thử nghiệm).
  - [ ] Quy trình chi tiết chạy thực nghiệm cho từng hệ mật.
- [ ] **Phần 4: Kết quả đạt được**
  - [ ] Bảng / biểu đồ tỷ lệ giải mã đúng theo độ dài văn bản.
  - [ ] Bảng / biểu đồ thời gian chạy trung bình của từng hệ mật.
  - [ ] So sánh đánh giá độ khó phá mã: Caesar (Dễ) $\rightarrow$ Vigenère (Trung bình) $\rightarrow$ Playfair (Khó).
- [ ] **Phần 5: Biện pháp phòng chống**
  - [ ] Phân tích lý do các hệ mật cổ điển không an toàn trong thực tế ngày nay.
  - [ ] Khuyến nghị sử dụng các thuật toán mã hóa hiện đại (AES, RSA, ECC).
  - [ ] Nguyên tắc chọn khóa đủ độ hỗn loạn (entropy), tránh dùng mật mã cổ điển trong hệ thống thực tế.

---

## 📊 3. Cấu trúc Slide Thuyết trình (25 - 40 Slide, Mẫu UTH)

> **Yêu cầu định dạng:** Dùng template mẫu UTH, Tiêu đề font size **32**, Nội dung font size **26**.

| Slide # | Nội dung | Trạng thái |
|:-------:|:---------|:----------:|
| 1 - 3 | **Mục tiêu dự án & Giới thiệu nhóm** | [ ] |
| 4 - 7 | **Cơ sở lý thuyết Caesar** | [ ] |
| 8 - 12 | **Cơ sở lý thuyết Vigenère** | [ ] |
| 13 - 17 | **Cơ sở lý thuyết Playfair** | [ ] |
| 18 - 21 | **Kịch bản thực nghiệm (Môi trường Lab & Docker)** | [ ] |
| 22 - 24 | **Kết quả thực nghiệm Caesar** | [ ] |
| 25 - 27 | **Kết quả thực nghiệm Vigenère** | [ ] |
| 28 - 30 | **Kết quả thực nghiệm Playfair** | [ ] |
| 31 - 33 | **Demo trực tiếp (Screenshot / Video demo)** | [ ] |
| 34 - 37 | **Biện pháp phòng chống & Khuyến nghị** | [ ] |
| 38 - 40 | **Kết luận & Q&A** | [ ] |

---

## ⚠️ 4. Quản lý Rủi ro & Lưu ý Kỹ thuật

- [ ] **Rủi ro Playfair attack mắc kẹt ở Cực trị Địa phương (Local Optimum)**:
  - *Giải pháp*: Triển khai kỹ thuật **Random Restart** lặp lại nhiều lần (ví dụ: 5.000 - 10.000 iterations). Cần tiến hành code phần này sớm từ Tuần 1 - 2.
- [ ] **Rủi ro Ciphertext quá ngắn**:
  - *Giải pháp*: Phân tích tần suất cần đủ dữ liệu. Cần thử nghiệm kiểm chứng với nhiều mức độ dài văn bản ($L = 50, 100, 500, 1000$ ký tự) để rút ra ngưỡng tối thiểu.
- [ ] **Rủi ro Thao tác Docker lúng túng khi Demo**:
  - *Giải pháp*: Thực hành chuẩn bị kỹ các lệnh `docker build` và `docker run -it` ngay trong Tuần 1 - 2.

---

## 📋 5. Checklist Nộp Bài Cuối Cùng (Final Verification)

- [ ] **Code**: Đầy đủ 3 module, chạy ổn định, không lỗi, đã đóng gói chạy tốt trong Docker container.
- [ ] **Báo cáo**: Đầy đủ 5 phần bắt buộc, đúng định dạng Markdown/Word/PDF theo yêu cầu.
- [ ] **Slide**: Đạt từ 25 - 40 slide, đúng mẫu UTH, chuẩn size chữ (Tiêu đề 32, Nội dung 26).
- [ ] **Demo**: Sẵn sàng kịch bản demo trực tiếp với Docker và ciphertext mẫu.
