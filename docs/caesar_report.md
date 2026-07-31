# Báo cáo Lý thuyết & Thử nghiệm: Mật mã Caesar

**Người thực hiện:** Người A

---

## 1. Lý thuyết Mật mã Caesar
- **Nguyên lý mã hóa:** Phép dịch vòng $k$ vị trí trong bảng chữ cái ($0 \le k \le 25$).
  $$C_i = (P_i + k) \pmod{26}$$
- **Nguyên lý giải mã:**
  $$P_i = (C_i - k) \pmod{26}$$

---

## 2. Phương pháp Thám mã (Cryptanalysis)
- **Phương pháp:** Brute-force tất cả 25 khóa có thể có.
- **Đánh giá văn bản:** Với mỗi khóa $k$, tính điểm Chi-squared ($\chi^2$) so với tần suất chữ cái tiếng Anh chuẩn:
  $$\chi^2 = \sum_{c=\text{'A'}}^{\text{'Z'}} \frac{(O_c - E_c)^2}{E_c}$$
  Trong đó:
  - $O_c$: Tần suất xuất hiện thực tế của chữ cái $c$ trong văn bản giải mã thử.
  - $E_c$: Tần suất kỳ vọng của chữ cái $c$ trong tiếng Anh chuẩn.
- Khóa $k$ cho điểm $\chi^2$ nhỏ nhất sẽ được chọn là khóa đúng.

---

## 3. Kết quả Thử nghiệm & Đánh giá
- **Độ dài ciphertext thử nghiệm:** ...
- **Kết quả thu được:** ...
