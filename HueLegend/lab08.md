# LAB 08 — KHỞI TẠO CẤU TRÚC DỰ ÁN NHÓM: HUELEGEND

- **Đề tài:** Truy xuất nguồn gốc đặc sản Huế trên Blockchain (HueLegend)
- **Bài toán:** Cơ sở sản xuất làng nghề và khách mua cần lịch sử lô hàng bất biến, chống hàng giả mạo.
- **Luồng cốt lõi demo:** Tạo lô → Thêm chặng bởi đúng vai → Quét QR xem lịch sử.

---

## Danh mục tài liệu và mã nguồn đã hoàn thiện

1. 📄 **Tài liệu đặc tả & Kế hoạch:**
   - [`README.md`](./README.md): Giới thiệu sản phẩm, bài toán và hướng dẫn sử dụng.
   - [`AGENTS.md`](./AGENTS.md): Quy ước kỹ thuật và nguyên tắc sinh mã cho AI (Solidity ^0.8.20, CEI, tiếng Việt không dấu,...).
   - [`docs/PROJECT_PLAN.md`](./docs/PROJECT_PLAN.md): Phân công vai trò thành viên và kế hoạch từ Lab 8 đến Lab 15.
   - [`docs/SPEC.md`](./docs/SPEC.md): Đặc tả nghiệp vụ luồng tạo lô, thêm chặng theo vai và quét mã QR.
   - [`docs/AI_JOURNAL.md`](./docs/AI_JOURNAL.md): Nhật ký làm việc cùng AI, các lỗ hổng mạo danh vai trò và tối ưu gas.
   - [`docs/ECONOMIC_RULES.md`](./docs/ECONOMIC_RULES.md): Quy tắc kinh tế, ký quỹ uy tín và chế tài xử lý gian lận (tính theo basis point).
   - [`docs/PRESENTATION_PLAN.md`](./docs/PRESENTATION_PLAN.md): Kịch bản thuyết trình và các bước thao tác live demo.

2. ⛓️ **Hợp đồng thông minh & Bài mẫu học tập:**
   - [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol): Smart contract cốt lõi của HueLegend.
   - [`contracts/training/`](./contracts/training/): Bài mẫu kỹ thuật dùng cho Lab 9, 10, 13 (`ClassPoint.sol`, `TimeLockVault.sol`, `VaultBuggy.sol`, `VulnerableBank.sol`).

3. 🧪 **Kiểm thử tự động:**
   - [`test/ProjectCore.test.js`](./test/ProjectCore.test.js): Bộ ca kiểm thử đơn vị, bao gồm ca kiểm thử gian lận (TC-03) khi kẻ xấu cố tình chèn chặng giả.

4. 🌐 **Giao diện Web3 DApp:**
   - [`web/index.html`](./web/index.html): Giao diện DApp phong cách Cố Đô hoàng gia, tích hợp sinh mã QR động và tra cứu timeline.

5. 📁 **Hồ sơ bằng chứng thực hành:**
   - [`evidence/lab-08/README.md`](./evidence/lab-08/README.md): Biên bản nộp bài Lab 8 và commit chuẩn.

---

## Mẫu commit kết thúc buổi thực hành Lab 8:
```bash
lab-08: [khoi tao cau truc du an HueLegend]
```
