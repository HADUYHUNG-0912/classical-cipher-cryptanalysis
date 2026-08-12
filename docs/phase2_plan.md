# 📋 KẾ HOẠCH GIAI ĐOẠN 2 (PHASE 2) — Cryptanalysis Toolkit

> **Người lập:** Hưng (Trưởng nhóm) · **Trạng thái:** Khởi tạo · **Cập nhật:** 10/08/2026
> File này bổ sung cho [`docs/checklist.md`](./checklist.md) — tập trung vào phần việc **còn lại sau khi code hoàn tất**.

---

## 1. Tổng quan

### ✅ Phase 1 — ĐÃ HOÀN THÀNH (đã merge vào `main`, đồng bộ remote)
- Cấu trúc dự án, `utils/` (frequency, text_utils), dữ liệu tần suất `data/`
- 3 module mã hóa + thám mã, có docstring + unit tests:
  - **Caesar** — brute-force 25 khóa + Chi-squared ✅ (8/8 test pass)
  - **Vigenère** — IC ước lượng key length + phá từng cột ✅ (5/5 test pass)
  - **Playfair** — Hill-climbing + Random Restart ✅ (5/5 test pass, chạy không lỗi)
- Dockerfile, `main.py` (CLI), 5 file báo cáo mẫu

### 🎯 Phase 2 — Mục tiêu
Biến bộ code đang chạy thành **sản phẩm demo hoàn chỉnh đủ điều kiện nộp bài**:
thực nghiệm + số liệu, Docker ổn định, báo cáo 5 phần, slide thuyết trình UTH, video demo.

---

## 2. Hiện trạng & các vấn đề cần xử lý trước (đã kiểm chứng)

| # | Vấn đề | Mức độ | Người phụ trách |
|---|--------|--------|-----------------|
| 1 | `python main.py` **crash trên console Windows** — lỗi `UnicodeEncodeError` (chữ tiếng Việt, encoding cp1252) | 🔴 Cao (demo local) | Hưng |
| 2 | **Playfair attack chưa đủ mạnh** — không tìm ra khóa với văn bản 400 ký tự (400 iterations × 3 restarts). Nghi do chấm điểm bigram *chồng lấp* thay vì theo cặp digraph + iterations thấp | 🔴 Cao (đây là phần khó nhất của đồ án) | Hiếu |
| 3 | **Test Caesar & Vigenère không chạy bằng `python -m unittest`** (viết hàm thường, không phải `unittest.TestCase`) → test suite chưa chuẩn hóa | 🟠 Trung bình | Hưng (hoặc Duy) |
| 4 | **Ciphertext quá ngắn → phá mã sai** (vd: `KHOOR ZRUOG` → key 6 thay vì 3) | 🟡 Đã biết (giới hạn tần suất) | Cả nhóm — ghi vào báo cáo |
| 5 | **Docker daemon chưa chạy** (đã cài v29.6.2) → chưa test `docker build` | 🟠 Trung bình | Hưng |

---

## 3. Phân công nhiệm vụ chi tiết

### 👤 Hưng — Trưởng nhóm + Caesar

| # | Nhiệm vụ | Deliverable | Deadline |
|---|----------|-------------|----------|
| ✅ H1 | Fix lỗi Unicode `main.py` (bật UTF-8 stdout hoặc đổi menu sang tiếng Anh) | `main.py` chạy được trên Windows lẫn Docker | Đã xong |
| ✅ H2 | Tạo thư mục `experiments/` + script đo tỷ lệ phá mã chung (dùng chung cả 3 module) | `experiments/benchmark.py` (input: module, độ dài L, số lần lặp) | Đã xong |
| ✅ H3 | Chạy thực nghiệm **Caesar**: L = 50/100/500/1000, mỗi mức N lần → tỷ lệ thành công + thời gian TB | Bảng số liệu + biểu đồ | Đã xong |
| ✅ H4 | Đóng gói & kiểm tra Docker: `docker build -t crypto-lab .` + `docker run -it crypto-lab` | Container chạy đủ 3 menu | Đã xong |
| H5 | Điền kết quả thực nghiệm vào `docs/caesar_report.md` (mục 3) | Báo cáo Caesar hoàn chỉnh | Tuần 3 |
| H6 | Quản lý nhóm: review code 2 bạn, merge PR vào `main`, push lên GitHub | Repo sạch, main luôn chạy được | Liên tục |

### 👤 Nguyễn Ánh Duy — Vigenère

| # | Nhiệm vụ | Deliverable | Deadline |
|---|----------|-------------|----------|
| D1 | Thực nghiệm **Vigenère**: key length 2→10 × độ dài L = 50/100/500/1000 → đo độ chính xác của IC khi ước lượng key length và tỷ lệ phá đúng | Bảng số liệu + biểu đồ | Tuần 2 |
| D2 | Chuẩn hóa `tests/test_vigenere.py` thành `unittest.TestCase` (để `python -m unittest` chạy được) | Test suite chuẩn | Tuần 2 |
| D3 | Điền kết quả thực nghiệm vào `docs/vigenere_report.md` (mục 3) | Báo cáo Vigenère hoàn chỉnh | Tuần 3 |

### 👤 Minh Hiếu — Playfair (ưu tiên cao nhất)

| # | Nhiệm vụ | Deliverable | Deadline |
|---|----------|-------------|----------|
| P1 | **Cải thiện `playfair/attack.py`**: ① chấm điểm theo **non-overlapping digraph** (đúng bản chất Playfair mã hóa theo cặp) thay vì bigram chồng lấp; ② tăng `iterations` (vd 5000–10000) & `restarts`; ③ thử thêm **simulated annealing** (chấp nhận bước xấu với xác suất giảm dần) để thoát local optimum | Attack phá được văn bản thực nghiệm (≥ 200 ký tự) | Tuần 2 |
| P2 | Thực nghiệm **Playfair**: tỷ lệ thành công theo L (100/200/500/1000) và theo iterations | Bảng số liệu + biểu đồ | Tuần 2 |
| P3 | Điền kết quả thực nghiệm vào `docs/playfair_report.md` (mục 3) | Báo cáo Playfair hoàn chỉnh | Tuần 3 |

### 👥 Cả nhóm

| # | Nhiệm vụ | Deliverable | Deadline |
|---|----------|-------------|----------|
| G1 | Viết phần chung: Mục tiêu, Kịch bản Lab Docker, Biện pháp phòng chống → ghép vào `docs/final_report.md` (đủ 5 phần bắt buộc) | Báo cáo tổng hoàn chỉnh | Tuần 3 |
| G2 | Review chéo báo cáo (lỗi chính tả, công thức toán, định dạng) | Bản dự thảo cuối | Tuần 3 |
| G3 | Soạn **slide 25–40** theo mẫu UTH (Tiêu đề 32pt, Nội dung 26pt), chia phần theo thuật toán từng người | File slide | Tuần 4 |
| G4 | Kịch bản demo (chạy Docker trước lớp) + quay video dự phòng | Video demo | Tuần 4 |
| G5 | Tổng duyệt cuối: Code + Báo cáo + Slide + Docker → nộp bài | Sản phẩm nộp | Tuần 4 |

---

## 4. Lộ trình theo tuần

| Tuần | Trọng tâm | Mốc hoàn thành (Milestone) |
|------|-----------|----------------------------|
| **Tuần 2** (còn lại) | Fix main.py · Thực nghiệm cả 3 hệ · Cải thiện Playfair attack · Docker build/run | ✅ 3 attack chạy ổn định trong Docker, có số liệu thực nghiệm đầy đủ |
| **Tuần 3** | Viết báo cáo thành phần + tổng hợp `final_report.md` · Review chéo | ✅ Báo cáo hoàn chỉnh bản nháp |
| **Tuần 4** | Slide UTH · Demo + video · Tổng duyệt · Nộp | ✅ Sản phẩm sẵn sàng demo & nộp |

> Tham chiếu chi tiết tick-list từng tuần tại [`docs/checklist.md`](./checklist.md).

---

## 5. Tiêu chí chấp nhận (Definition of Done)

- [ ] `main.py` chạy được trên Windows local **và** trong Docker (đủ 3 menu, không crash)
- [ ] Playfair attack tìm lại đúng plaintext với văn bản ≥ 200 ký tự (tối thiểu ở mức thực nghiệm)
- [ ] `python -m unittest discover -s tests` chạy được **toàn bộ** 3 module (≥ 15 test) — cần chuẩn hóa test Caesar & Vigenère
- [ ] `experiments/` có script benchmark + bảng số liệu (tỷ lệ % theo L, thời gian TB) cho từng module
- [ ] `docs/final_report.md` đủ 5 phần bắt buộc (Mục tiêu / Lý thuyết / Kịch bản Lab / Kết quả / Phòng chống)
- [ ] Slide 25–40 đúng mẫu UTH, có video demo dự phòng
- [ ] Tất cả commit push lên GitHub qua feature branch + PR (không push thẳng `main`)

---

## 6. Rủi ro & biện pháp

| Rủi ro | Biện pháp |
|--------|-----------|
| Playfair attack mắc kẹt local optimum | Random Restart 5000–10000 iterations + simulated annealing (P1) |
| Ciphertext ngắn → tần suất không ổn định | Xác định ngưỡng tối thiểu từ thực nghiệm (L ≥ 100), ghi rõ trong báo cáo |
| Lúng túng khi demo Docker trước lớp | Tập luyện trước + chuẩn bị video dự phòng (G4) |
| Xung đột khi merge (3 người sửa code cùng lúc) | Làm trên feature branch riêng, merge qua PR, ai sửa file nào rõ ràng |
| Máy Windows không chạy được tiếng Việt trong console | Fix encoding main.py (H1) — ưu tiên cao |

---

## 7. Quy trình Git cho Phase 2

```bash
# Mỗi thành viên làm trên nhánh riêng từ main (không push thẳng main)
git checkout main && git pull
git checkout -b <tên>/phase2-<nội-dung>   # vd: hieu/improve-playfair-attack
# ... làm việc, commit, push
git push -u origin <nhánh>
# Tạo Pull Request → Leader (Hưng) review → merge vào main
```

- Commit convention: `feat(...)`, `fix(...)`, `docs(...)`, `test(...)` (tiếng Anh, ngắn gọn)
- Sau mỗi PR: chạy `python -m unittest discover -s tests` trước khi merge

---

## 8. Checklist nộp bài cuối cùng (tóm tắt — chi tiết tại `docs/checklist.md`)

- [ ] **Code:** 3 module chạy ổn định trong Docker
- [ ] **Báo cáo:** đủ 5 phần, đúng định dạng Markdown/Word/PDF
- [ ] **Slide:** 25–40 slide, mẫu UTH, chuẩn font size
- [ ] **Demo:** kịch bản + video dự phòng sẵn sàng

---

*📌 Ghi chú: Phase 2 ước tính 2 tuần rưỡi làm việc tích cực (bắt đầu ngay sau khi code merge xong). Deadline nộp bài theo lịch của giảng viên — cập nhật vào file này khi có thông tin chính thức.*
