# PRESENTATION_PLAN — KỊCH BẢN DEMO VÀ PHÂN CÔNG TRÌNH BÀY DỰ ÁN HUELEGEND

- **Thời lượng dự kiến:** 5 – 7 phút thuyết trình + 3 phút hỏi đáp (Q&A).
- **Trang phục / Thiết bị:** Đồng phục nhóm, 01 laptop điều khiển DApp chiếu màn hình lớn, 01 điện thoại di động để quét mã QR trực tiếp.

---

## 1. Phân công trình bày chi tiết

| Thời lượng | Người trình bày | Nội dung trọng tâm | Slide / Màn hình hiển thị |
| :--- | :--- | :--- | :--- |
| **0:00 – 2:30** | **Ngô Thị Thuỷ Vân** *(Trưởng nhóm)* | - Mở đầu & Vấn đề: Đặc sản Huế bị nhái nhãn mác, khách hàng mất niềm tin.<br>- Giới thiệu giải pháp Web3 HueLegend.<br>- Kiến trúc kỹ thuật, Smart Contract `ProjectCore.sol` & Demo bước 1 (Khởi tạo lô đặc sản). | Slide 1 – 4 & Thao tác DApp |
| **2:30 – 5:30** | **Ngô Quỳnh Trang** | - Demo bước 2: Thêm chặng theo đúng vai (Logistics, Retailer, Inspector).<br>- Demo ca gian lận: Mạo danh vai trò bị chặn (`revert UnauthorizedCaller`).<br>- Demo bước 3: Quét mã QR bằng điện thoại xem Timeline minh bạch. | Trực tiếp trên giao diện `web/index.html` và Etherscan |
| **5:30 – 6:30** | **Cả hai thành viên** | - Tổng kết tiến độ từ Lab 8 đến Lab 15.<br>- Định hướng mở rộng số hóa làng nghề Huế.<br>- Lắng nghe và trả lời câu hỏi phản biện của Giảng viên. | Slide kết thúc & Q&A |

---

## 2. Kịch bản thao tác Live Demo (Chi tiết từng click chuột)

### Bước 1: Khởi tạo lô hàng đặc sản (Role: PRODUCER)
- Thao tác: Mở tab **"Khởi tạo Lô hàng"** trên DApp.
- Dữ liệu nhập mẫu:
  - Mã lô: `HL-MEXUNG-2026-001`
  - Tên đặc sản: `Mè xửng Thiên Hương Thượng Hạng`
  - Vùng nguyên liệu: `Phú Hậu, TP Huế`
  - Chuẩn OCOP: `OCOP 4 sao tỉnh Thừa Thiên Huế`
- Bấm nút: **"Tạo Lô Hàng On-chain"**.
- Kết quả: Hệ thống ghi nhận giao dịch thành công, lập tức xuất hiện mã QR code động cho lô hàng này.

### Bước 2: Thêm chặng theo đúng vai trò & Thử nghiệm gian lận
- **Thử nghiệm gian lận (Fraud Prevention Demo):**
  - Giả lập ví của Kẻ xấu chưa được cấp quyền cố tình bấm cập nhật chặng kiểm định giả mạo.
  - Kết quả: DApp và Hợp đồng thông minh báo lỗi lập tức: `UnauthorizedCaller`!
- **Thao tác đúng vai (Role: LOGISTICS):**
  - Chuyển sang ví của Đơn vị vận chuyển (hoặc chọn vai trò Logistics đã được cấp quyền).
  - Nhập địa điểm: `Ga Huế, Phường Đúc, TP Huế`.
  - Hành động: `Đóng thùng chống ẩm, xuất kho tàu hỏa đi Hà Nội`.
  - Bấm nút: **"Cập nhật Chặng"**.
  - Kết quả: Giao dịch thành công, chặng được nối thêm vào lịch sử chuỗi cung ứng.

### Bước 3: Khách hàng quét mã QR xem lịch sử minh bạch
- Thao tác: Khách hàng (dùng camera điện thoại hoặc tab **"Tra cứu & Quét QR"**) quét mã QR của sản phẩm.
- Màn hình hiển thị:
  - Thông tin đầy đủ của lô hàng, huy hiệu xác thực làng nghề Huế.
  - Timeline trực quan từng chặng kèm dấu thời gian chính xác, địa chỉ ví người ký xác thực và liên kết kiểm tra mã băm giao dịch (TxHash) trên Sepolia Etherscan.

---

## 3. Các câu hỏi phản biện dự kiến (Q&A Preparation)

1. **Hỏi:** *Tại sao lại dùng Blockchain cho bài toán này thay vì cơ sở dữ liệu truyền thống SQL?*
   - **Trả lời:** Cơ sở dữ liệu tập trung hoàn toàn có thể bị quản trị viên sửa đổi dữ liệu ngày sản xuất hoặc tẩy xóa lịch sử lô hàng hỏng. Với Blockchain, dữ liệu một khi đã ghi on-chain là vĩnh viễn và bất biến, tạo niềm tin tuyệt đối cho khách du lịch khi mua đặc sản giá trị cao.

2. **Hỏi:** *Làm thế nào để đảm bảo người vận chuyển không khai báo thông tin giả mạo?*
   - **Trả lời:** Hệ thống áp dụng chữ ký số của ví Web3 tương ứng với từng vai trò (`ROLE_LOGISTICS`). Nếu thông tin sai lệch, dấu vết on-chain gắn chặt với danh tính ví của đơn vị đó, dẫn đến việc bị trừ điểm tín nhiệm và tịch thu tiền ký quỹ bảo đảm (`ECONOMIC_RULES.md`).
