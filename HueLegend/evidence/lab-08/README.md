# BẰNG CHỨNG THỰC HÀNH LAB 8 — DỰ ÁN HUELEGEND

- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Tên dự án nhóm:** **HueLegend** — Truy xuất nguồn gốc đặc sản Huế trên Blockchain
- **Tiêu đề commit nộp bài:**
  ```bash
  lab-08: [khoi tao cau truc du an HueLegend]
  ```

---

## 1. Kết quả thực hiện trong Lab 8

1. **Khởi tạo cấu trúc thư mục nhóm chuẩn hóa:**
   - Hoàn thiện đầy đủ cây thư mục theo yêu cầu thống nhất từ Lab 8 của học phần ECO2432 (`README.md`, `AGENTS.md`, `docs/`, `contracts/`, `test/`, `web/`, `evidence/`).
2. **Xây dựng tài liệu đặc tả và kế hoạch dự án:**
   - [`PROJECT_PLAN.md`](../../docs/PROJECT_PLAN.md): Phân công vai trò nhóm và lộ trình chi tiết từ Lab 8 đến Lab 15.
   - [`SPEC.md`](../../docs/SPEC.md): Đặc tả nghiệp vụ luồng cốt lõi: Tạo lô → Thêm chặng theo đúng vai → Quét QR tra cứu lịch sử.
   - [`ECONOMIC_RULES.md`](../../docs/ECONOMIC_RULES.md): Quy tắc kinh tế, ký quỹ bảo đảm uy tín và chế tài xử lý gian lận nguồn gốc (sử dụng basis point).
   - [`AI_JOURNAL.md`](../../docs/AI_JOURNAL.md): Nhật ký làm việc cùng AI, phát hiện và khắc phục các lỗ hổng mạo danh vai trò và tối ưu gas.
   - [`PRESENTATION_PLAN.md`](../../docs/PRESENTATION_PLAN.md): Kịch bản thuyết trình bảo vệ đề tài và các bước live demo.
3. **Triển khai Smart Contract cốt lõi:**
   - [`ProjectCore.sol`](../../contracts/project/ProjectCore.sol): Hợp đồng thông minh quản lý lô hàng đặc sản Huế, tuân thủ nghiêm ngặt chuẩn OpenZeppelin 5.x, Solidity `^0.8.20`, Checks-Effects-Interactions, Custom Errors và chú thích tiếng Việt không dấu.
4. **Bộ kiểm thử toàn diện:**
   - [`ProjectCore.test.js`](../../test/ProjectCore.test.js): Bao gồm các ca kiểm thử hợp lệ và ca kiểm thử gian lận (TC-03) khi kẻ xấu cố tình chèn chặng giả.
5. **Giao diện người dùng Web3 DApp:**
   - [`web/index.html`](../../web/index.html): Giao diện tương tác hiện đại mang đậm bản sắc cố đô Huế, hỗ trợ tạo lô hàng, cập nhật chặng theo vai và quét mã QR sinh động.

---

## 2. Minh chứng hình ảnh và mã băm giao dịch (TxHash)

*(Các hình ảnh chụp màn hình thao tác và bằng chứng thực nghiệm trên mạng Sepolia sẽ được lưu trữ tại thư mục này)*.
