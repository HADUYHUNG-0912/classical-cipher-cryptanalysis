# Báo cáo Lý thuyết & Thử nghiệm: Mật mã Vigenère

**Người thực hiện:** Nguyễn Ánh Duy

---

## 1. Lý thuyết Mật mã Vigenère
- **Nguyên lý:** Mã hóa thay thế nhiều bảng chữ cái (polyalphabetic substitution) sử dụng từ khóa $K = (k_0, k_1, \dots, k_{m-1})$ độ dài $m$.
- **Công thức:**
  $$C_i = (P_i + K_{i \pmod m}) \pmod{26}$$

---

## 2. Phương pháp Thám mã (Cryptanalysis)
### Bước 1: Ước lượng độ dài khóa ($m$)
- **Phương pháp 1: Kasiski Examination** — Tìm các chuỗi lặp lại trong ciphertext và tính ước chung của khoảng cách giữa chúng.
- **Phương pháp 2: Index of Coincidence (IC)** — Tính chỉ số trùng hợp cho các chuỗi con cách nhau $m$ ký tự. IC của tiếng Anh chuẩn $\approx 0.067$.

### Bước 2: Phá khóa từng vị trí
- Tách ciphertext thành $m$ nhóm ký tự độc lập.
- Áp dụng thuật toán thám mã Caesar (Chi-squared test) cho từng nhóm để tìm ký tự tương ứng của khóa $K$.

---

## 3. Kết quả Thử nghiệm & Đánh giá
- **Độ dài khóa thử nghiệm:** ...
- **Độ dài ciphertext tối thiểu để phá thành công:** ...
