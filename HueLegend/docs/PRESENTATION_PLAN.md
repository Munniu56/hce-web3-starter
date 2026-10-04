# PRESENTATION_PLAN — KỊCH BẢN DEMO VÀ PHÂN CÔNG TRÌNH BÀY DỰ ÁN HUELEGEND

- **Thời lượng dự kiến:** 5 – 7 phút thuyết trình + 3 phút hỏi đáp (Q&A).
- **Trang phục / Thiết bị:** Đồng phục nhóm, 01 laptop điều khiển DApp chiếu màn hình lớn, 01 điện thoại di động để quét mã QR trực tiếp.

---

## 1. Phân công trình bày chi tiết

| Thời lượng | Người trình bày | Nội dung trọng tâm | Slide / Màn hình hiển thị |
| :--- | :--- | :--- | :--- |
| **0:00 – 1:30** | **Thành viên 01** *(Lead)* | - Mở đầu & Nỗi đau thị trường: Đặc sản Huế bị làm giả, nhái nhãn mác tràn lan tại các điểm du lịch.<br>- Khách mua không phân biệt được thật giả; Cơ sở làng nghề uy tín bị tổn hại.<br>- Giới thiệu giải pháp: **HueLegend** — Truy xuất nguồn gốc bằng Smart Contract bất biến. | Slide 1 – 3: Vấn đề & Kiến trúc giải pháp |
| **1:30 – 3:00** | **Thành viên 02** *(SC Dev)* | - Trình bày mô hình dữ liệu: Lô hàng (`Batch`) và Chặng (`Checkpoint`).<br>- Cơ chế phân quyền RBAC: Phân tách vai trò Cơ sở sản xuất, Đơn vị vận chuyển, Đại lý phân phối.<br>- Quy tắc an toàn: CEI, Custom Errors, phòng chống mạo danh chặng giả. | Slide 4 – 5 & Mã nguồn `ProjectCore.sol` trên Remix/IDE |
| **3:00 – 5:30** | **Thành viên 03 & 04** *(Demo Lead)* | **Thực hiện Live Demo luồng 3 bước:**<br>1. *Tạo lô:* Kết nối ví cơ sở sản xuất, tạo lô "Mè xửng Thiên Hương #001", sinh mã QR.<br>2. *Thêm chặng:* Đơn vị vận chuyển xác nhận nhận hàng tại Ga Huế.<br>3. *Demo chống gian lận:* Ví kẻ xấu cố tình chèn chặng giả → Hệ thống từ chối giao dịch.<br>4. *Quét QR:* Dùng camera điện thoại quét mã QR hiển thị dòng thời gian minh bạch. | Trực tiếp trên giao diện DApp `web/index.html` và Etherscan Sepolia |
| **5:30 – 6:30** | **Cả nhóm** | - Tổng kết kết quả đạt được qua các Lab (từ Lab 8 đến Lab 15).<br>- Định hướng mở rộng: Tích hợp cảm biến IoT và số hóa các làng nghề tôm chua, nón bài thơ.<br>- Cảm ơn và sẵn sàng trả lời phản biện của Giảng viên. | Slide kết & Bảng phân bổ đóng góp nhóm |

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
