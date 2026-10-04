# KẾ HOẠCH DỰ ÁN HUELEGEND (PROJECT PLAN)

## 1. Thông tin chung dự án
- **Tên dự án:** HueLegend — Nền tảng Truy xuất Nguồn gốc Đặc sản Huế trên Blockchain
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432 / TDT&HDTM)
- **Mục tiêu:** Xây dựng hệ thống Web3 DApp hoàn chỉnh cho phép Cơ sở sản xuất tạo lô hàng đặc sản, các đơn vị chuỗi cung ứng thêm chặng hành trình theo đúng vai trò, và người tiêu dùng quét mã QR để tra cứu lịch sử bất biến.

---

## 2. Phân công vai trò trong nhóm

| Thành viên | Vai trò phụ trách | Trách nhiệm chính |
| :--- | :--- | :--- |
| **Ngô Thị Thuỷ Vân** | **Trưởng nhóm / Product Owner & SC Dev** | Quản lý tiến độ, thiết kế kiến trúc hệ thống, phát triển Smart Contract `ProjectCore.sol`, thiết lập môi trường kiểm thử. |
| **Thành viên 02** | **Frontend Web3 Developer** | Xây dựng giao diện DApp (`web/index.html`), tích hợp thư viện Ethers.js, QR Code Generator và hiển thị Timeline tương tác. |
| **Thành viên 03** | **QA & Smart Contract Auditor** | Soạn thảo kịch bản kiểm thử (`test/`), thẩm định an toàn bảo mật, mô phỏng các ca tấn công gian lận và kiểm tra gas. |
| **Thành viên 04** | **Business Analyst & Content Lead** | Hoàn thiện tài liệu nghiệp vụ (`SPEC.md`, `ECONOMIC_RULES.md`, `PRESENTATION_PLAN.md`), chuẩn bị dữ liệu mẫu các làng nghề đặc sản Huế. |

---

## 3. Lộ trình công việc chi tiết (Từ Lab 8 đến Lab 15)

| Mốc (Milestone) | Nội dung công việc chính | Kết quả đầu ra (Deliverables) |
| :--- | :--- | :--- |
| **Lab 8** *(Hiện tại)* | - Khởi tạo cấu trúc chuẩn của dự án `HueLegend`<br>- Viết `SPEC.md`, `AGENTS.md`, `ECONOMIC_RULES.md`<br>- Triển khai hợp đồng `ProjectCore.sol` đáp ứng luồng cốt lõi: Tạo lô → Thêm chặng theo vai → Quét QR<br>- Viết bộ kiểm thử gồm ca gian lận<br>- Dựng giao diện Web DApp mẫu | Cấu trúc thư mục hoàn thiện, hợp đồng `ProjectCore.sol` biên dịch sạch, giao diện web chạy được, commit `lab-08: [khoi tao cau truc du an HueLegend]` |
| **Lab 9** | - Nghiên cứu kỹ thuật qua các hợp đồng `contracts/training/`<br>- Tối ưu hóa lưu trữ và chi phí gas cho struct Lô hàng và Chặng | Báo cáo phân tích gas, tối ưu kiểu dữ liệu `uint256`, `string` sang `bytes32` |
| **Lab 10** | - Hoàn thiện cơ chế phân quyền RBAC (Role-Based Access Control) nhiều cấp<br>- Xây dựng chức năng cấp/hủy quyền cơ sở sản xuất và điểm bán | Cập nhật hợp đồng, bổ sung test case kiểm tra phân quyền nâng cao |
| **Lab 11** | - Triển khai hợp đồng lên mạng thử nghiệm **Ethereum Sepolia Testnet**<br>- Thực hiện xác thực mã nguồn trên Sepolia Etherscan | Địa chỉ Contract Sepolia, link Etherscan đã verified, lưu TxHash vào `evidence/lab-11` |
| **Lab 12** | - Cụ thể hóa quy tắc kinh tế số (`ECONOMIC_RULES.md`)<br>- Mô phỏng cơ chế ký quỹ (Staking) bảo đảm chất lượng của làng nghề | Hợp đồng có tích hợp tiền cọc đảm bảo, ca kiểm thử phạt tịch thu cọc khi gian lận |
| **Lab 13** | - Kiểm thử bảo mật chuyên sâu (Security Audit)<br>- Rà soát các lỗi phổ biến (Reentrancy, Integer Overflow, Denial of Service khi duyệt mảng chặng) | Báo cáo kiểm định an toàn, cập nhật `AI_JOURNAL.md` ghi nhận lỗi phát hiện |
| **Lab 14** | - Tích hợp toàn diện giao diện Web3 với ví MetaMask và Sepolia RPC<br>- Tích hợp chức năng tạo mã QR động dẫn thẳng đến trang tra cứu lô hàng | Giao diện DApp hoạt động mượt mà với ví thực tế, quét camera QR trực tiếp |
| **Lab 15** | - Diễn tập kịch bản bảo vệ (`PRESENTATION_PLAN.md`)<br>- Tổng hợp toàn bộ hồ sơ bằng chứng từ Lab 8 - 15 vào thư mục `evidence/` | Video/Slide báo cáo, đường link chạy thật (Vercel/GitHub Pages), bảo vệ thành công |
