# ECO2432 — Tiền điện tử & Hợp đồng thông minh (Web3 Starter)

Kho lưu trữ mã nguồn và hồ sơ thực hành cá nhân xuyên suốt các bài thực hành học phần **ECO2432 - Tiền điện tử và Hợp đồng thông minh (TDT&HDTM)**.

---

## 📌 Thông tin sinh viên

- **Họ và tên:** Ngô Thị Thuỷ Vân
- **Mã sinh viên:** `23K4300023`
- **Lớp:** K57 - Kinh tế số
- **Môn học:** Tiền điện tử & Hợp đồng thông minh (ECO2432 / TDT&HDTM)
- **Địa chỉ ví Sepolia Testnet:** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **GitHub Repository:** [https://github.com/Munniu56/hce-web3-starter](https://github.com/Munniu56/hce-web3-starter)

---

## 🚀 Bắt đầu (Môi trường làm việc)

Kho lưu trữ được thiết lập và quản lý trực tiếp qua Antigravity IDE:

1. Mở thư mục dự án bằng **Antigravity IDE**.
2. Đọc kỹ [`AGENTS.md`](./AGENTS.md) trước khi yêu cầu trợ lý AI sinh mã hoặc cấu hình hợp đồng thông minh.
3. Cập nhật và lưu trữ [`SPEC.md`](./SPEC.md) và [`AI_JOURNAL.md`](./AI_JOURNAL.md) cho từng bài thực hành.
4. **An toàn bảo mật:** Chỉ sử dụng ví thử nghiệm trên mạng **Ethereum Sepolia Testnet**; tuyệt đối không dùng khóa bí mật (private key) của ví có tiền thật.

### Đưa mã nguồn lên GitHub

```bash
git init -b main
git add .
git commit -m "chore: thiet lap moi truong lam viec"
git remote add origin https://github.com/Munniu56/hce-web3-starter.git
git push -u origin main
```

> **Lưu ý với Lab 8 (Bài tập nhóm):** Một thành viên đại diện tạo repository trống mới trên GitHub, đẩy toàn bộ mã nguồn lên theo hướng dẫn trên, sau đó mời các thành viên còn lại làm cộng tác viên (collaborator).

---

## 📂 Cấu trúc thư mục

- [`AGENTS.md`](./AGENTS.md): Quy ước kỹ thuật dự án (Solidity ^0.8.20, OpenZeppelin 5.x, CEI pattern, quy tắc an toàn).
- [`Lab 1-7/`](./Lab%201-7/): Bằng chứng nộp bài, kịch bản phân tích dòng tiền và nhật ký thực hành từ Lab 1 đến Lab 7.
- `contracts/`:
  - `01_Basics/`: Các hợp đồng cơ bản mở đầu môn học.
  - `lab04/ClubTokens.sol`: Ba hợp đồng token phục vụ phân tích rủi ro trong Lab 4.
  - `training/`: Hợp đồng mẫu dùng cho Lab 9, 10, 11 và 13 (`TimeLockVault`, `VaultBuggy`, `ClassPoint`, `VulnerableBank`).
- `scripts/`: Kịch bản Python phân tích giao dịch on-chain qua Etherscan API.
- `web/`: Giao diện Web3 DApp mẫu (`index.html`) dùng trong Lab 15.
- [`SPEC.md`](./SPEC.md): Tài liệu đặc tả kỹ thuật và yêu cầu chức năng.
- [`AI_JOURNAL.md`](./AI_JOURNAL.md): Nhật ký chi tiết các phiên làm việc và thẩm định cùng AI.
- [`prompt_templates.md`](./prompt_templates.md): Mẫu câu lệnh có yêu cầu và tiêu chí kiểm chứng rõ ràng.

> **Lưu ý:** Các hợp đồng có chữ `Buggy`, `Vulnerable` hoặc có cảnh báo trong mã nguồn đều chứa lỗi có chủ đích nhằm phục vụ mục đích phân tích và học tập kiểm thử bảo mật.

---

## ⚙️ Hướng dẫn biên dịch & chạy hợp đồng

- **Cách chính (Khuyến nghị):** Mở [Remix IDE](https://remix.ethereum.org), tạo tệp và dán mã nguồn. Remix tự động tải thư viện `@openzeppelin/...` từ internet, không cần cài đặt thêm.
- **Biên dịch cục bộ:** Nếu Antigravity IDE báo gạch đỏ ở các dòng `import "@openzeppelin/..."`, đó là do máy chưa tải sẵn thư viện cục bộ (mã vẫn hoàn toàn hợp lệ). Để tắt cảnh báo, bạn có thể chạy:
  ```bash
  npm install
  ```
  *(Bước này không bắt buộc).*

---

## 🛡️ Quy tắc bắt buộc khi viết hợp đồng (Theo `AGENTS.md`)

1. Mọi hàm làm thay đổi trạng thái phải phát `event`.
2. Mọi hàm dành cho chủ sở hữu phải kiểm tra quyền rõ ràng.
3. Áp dụng nghiêm ngặt mô hình **Checks - Effects - Interactions**.
4. Chuyển ETH bằng `call{value: ...}("")` và kiểm tra kết quả; không dùng `transfer`.
5. Ưu tiên `error` tùy biến thay cho chuỗi lỗi dài.
6. Không dùng `tx.origin` để xác thực.
7. Tỷ lệ phần trăm dùng basis point, trong đó 1% = 100.
