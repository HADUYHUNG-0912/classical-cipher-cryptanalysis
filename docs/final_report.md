# Báo cáo Tổng hợp Đồ án Thám mã Mật mã Cổ điển

## 1. Giới thiệu tổng quan
- **Tên đồ án:** Cryptanalysis Toolkit (Caesar / Vigenère / Playfair)
- **Mục tiêu:** Tự động hóa quá trình thám mã (giải mã không biết khóa trước) cho 3 hệ mật mã cổ điển dựa trên phân tích tần suất ngôn ngữ.
- **Thành viên nhóm và phân công:**
  - **Người A:** Nghiên cứu & triển khai thám mã Caesar
  - **Người B:** Nghiên cứu & triển khai thám mã Vigenère
  - **Người C:** Nghiên cứu & triển khai thám mã Playfair

---

## 2. Kiến trúc Hệ thống & Luồng xử lý
- **Thư mục dự án:**
  - `caesar/`: Mã hóa, giải mã & thám mã Caesar
  - `vigenere/`: Mã hóa, giải mã & thám mã Vigenère
  - `playfair/`: Mã hóa, giải mã & thám mã Playfair
  - `utils/`: Các hàm dùng chung (xử lý văn bản, tính tần suất, Chi-squared, Index of Coincidence)
  - `data/`: Bảng tần suất chữ cái & bigram tiếng Anh chuẩn

---

## 3. Tổng kết Kết quả Thử nghiệm
| Hệ mật mã | Phương pháp thám mã | Tỷ lệ thành công | Ghi chú |
|-----------|----------------------|------------------|---------|
| **Caesar** | Brute-force 25 khóa + Chi-squared | | |
| **Vigenère** | Kasiski / IC + Giải từng cột Caesar | | |
| **Playfair** | Hill-Climbing / Simulated Annealing (Bigram) | | |

---

## 4. Kết luận & Hướng phát triển
- **Kết luận:** ...
- **Hướng phát triển:** ...
