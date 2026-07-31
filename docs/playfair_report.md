# Báo cáo Lý thuyết & Thử nghiệm: Mật mã Playfair

**Người thực hiện:** Người C

---

## 1. Lý thuyết Mật mã Playfair
- **Nguyên lý:** Mã hóa thay thế theo cặp chữ cái (digram substitution) dựa trên ma trận khóa $5 \times 5$ (gộp 'I' và 'J').
- **Quy tắc thay thế:**
  - Cùng hàng: dịch sang phải 1 cột.
  - Cùng cột: dịch xuống dưới 1 hàng.
  - Khác hàng & cột: tạo hình chữ nhật, lấy ký tự ở cùng hàng nhưng thuộc cột của ký tự đối diện.

---

## 2. Phương pháp Thám mã (Cryptanalysis)
- **Thách thức:** Số lượng ma trận khóa $5 \times 5$ rất lớn ($25! \approx 1.55 \times 10^{25}$), không thể brute-force.
- **Phương pháp giải quyết:** Thuật toán Leo đồi (Hill-Climbing Algorithm) / Simulated Annealing.
- **Hàm đánh giá (Fitness Function):** Chấm điểm văn bản giải mã dựa trên log-likelihood của tần suất cặp chữ cái (bigram frequency) trong tiếng Anh chuẩn:
  $$\text{Score} = \sum \log_{10}(P(\text{bigram}))$$
- **Quy trình lặp:**
  1. Khởi tạo ngẫu nhiên ma trận khóa $5 \times 5$.
  2. Thay đổi ngẫu nhiên ma trận (đổi chỗ 2 chữ cái, đảo hàng, đảo cột,...).
  3. Giải mã thử và chấm điểm score.
  4. Nếu score mới tốt hơn, chấp nhận ma trận mới. Lặp lại với Random Restarts để tránh bẫy cực trị địa phương (local optima).

---

## 3. Kết quả Thử nghiệm & Đánh giá
- **Số vòng lặp (iterations):** ...
- **Đánh giá độ chính xác tìm khóa:** ...
