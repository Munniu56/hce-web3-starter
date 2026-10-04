# PROJECT PLAN — HueLegend

## Thành viên và vai trò

Nhóm gồm 4 thành viên đảm nhận 4 vai trò chính: **Đặc tả**, **Hợp đồng**, **Giao diện**, **Kiểm thử**. Các thành viên thực hiện luân chuyển (xoay) vai trò từ sau Lab 11 theo đúng quy định học phần:

| Họ tên | Mã sinh viên | Vai chính Lab 8–11 | Vai chính Lab 12–15 |
| :--- | :--- | :--- | :--- |
| **Ngô Thị Thuỷ Vân** *(Trưởng nhóm)* | 23K4300023 | Hợp đồng (Smart Contract) | Kiểm thử (QA & Security Audit) |
| **Lê Thị Thảo Nhi** | 23K4300018 | Đặc tả (SPEC & BA Lead) | Giao diện (Frontend Web3 DApp) |
| **Trần Văn Nhật Minh** | 23K4300015 | Giao diện (Frontend Web3 DApp) | Đặc tả (SPEC & Gate Review) |
| **Nguyễn Hoàng Phúc** | 23K4300020 | Kiểm thử (Test Cases & Script) | Hợp đồng (Smart Contract Core) |

---

## Người dùng và vấn đề

- **Người dùng chính:**
  - *Cơ sở sản xuất & Làng nghề truyền thống Huế:* Các hộ kinh doanh, xưởng đặc sản (Mè xửng Thiên Hương, Tôm chua Trọng Tín, Trà Cung đình Đức Phượng, Nón lá Tây Hồ, Dầu tràm Lộc Thủy).
  - *Đơn vị chuỗi cung ứng:* Đơn vị logistics, bến bãi, đại lý/điểm bán lẻ quà lưu niệm tại Huế và các tỉnh thành.
  - *Khách mua hàng & Du khách:* Người tiêu dùng mua đặc sản Huế làm quà, cần kiểm chứng nguồn gốc chuẩn chỉ.
  - *Cơ quan thẩm định:* Chi cục Quản lý Chất lượng Nông Lâm Thủy sản, Ban quản lý OCOP tỉnh Thừa Thiên Huế.

- **Vấn đề cần giải quyết:**
  - Tình trạng hàng nhái, hàng trôi nổi kém chất lượng mạo danh đặc sản Huế làm suy giảm nghiêm trọng uy tín làng nghề.
  - Khách hàng thiếu công cụ tin cậy để đối soát thông tin; tem nhãn giấy truyền thống rất dễ bị làm giả, bóc dán tráo đổi.
  - Các bên vận chuyển, phân phối thiếu bằng chứng xác nhận trách nhiệm minh bạch, bất biến.

- **Sản phẩm cuối nhìn thấy được:**
  - DApp Web3 công khai (`web/index.html`) hỗ trợ kết nối ví Web3 (Ethereum Sepolia).
  - Luồng 3 bước hoạt động trơn tru: Tạo lô hàng $\rightarrow$ Thêm chặng theo đúng vai trò $\rightarrow$ Quét mã QR xem dòng thời gian (Timeline) lịch sử lô hàng bất biến on-chain.
  - Smart contract `ProjectCore.sol` đã triển khai và xác thực mã nguồn trên Sepolia Etherscan.

---

## Mốc bắt buộc

- **Lab 9:** contract lõi biên dịch được (tối ưu hóa gas và cấu trúc dữ liệu theo bài học training).
- **Lab 10:** audit và sửa lỗi có bằng chứng (kiểm tra phân quyền RBAC và các lỗ hổng Reentrancy, Overflow).
- **Lab 11:** quy tắc kinh tế chạy đúng (triển khai hợp đồng lên mạng Sepolia Testnet, kích hoạt cơ chế phí và cọc).
- **Lab 12:** Gate Review 1 (báo cáo đánh giá giữa kỳ và thẩm định tính khả thi của mô hình).
- **Lab 13:** test ca tấn công/gian lận (mô phỏng kẻ xấu cố tình tạo chặng giả mạo, chèn mã lô trùng, vượt quyền).
- **Lab 14:** audit chéo (phản biện và kiểm thử bảo mật chéo giữa các nhóm trong lớp).
- **Lab 15:** URL DApp công khai (bảo vệ dự án, live demo quét mã QR và trình diễn sản phẩm cuối kỳ).
