# SPEC — [Tên bài]
## 1. Mục đích
Một câu: hệ thống này giải quyết việc gì cho ai.

## 2. Đầu vào
- Một địa chỉ ví, dạng chuỗi 42 ký tự bắt đầu bằng 0x.
- Khóa API của Etherscan, đọc từ biến môi trường ETHERSCAN_API_KEY.
- Số ngày cần phân tích, mặc định 90.

## 3. Quy tắc nghiệp vụ
- R1: Giao dịch có trường "to" trùng địa chỉ đang xét được tính là dòng tiền vào.
- R2: Giao dịch có trường "from" trùng địa chỉ đang xét được tính là dòng tiền ra.
- R3: Với giao dịch đi ra, số tiền thực trừ khỏi ví = giá trị chuyển + phí giao dịch.
- R4: Giao dịch có trạng thái thất bại vẫn bị trừ phí, phải tính vào dòng tiền ra.
- R5: Mọi số tiền lấy về ở đơn vị wei, phải chia cho 10^18 trước khi hiển thị.
- R6: Sắp xếp theo thời gian tăng dần.

## 4. Đầu ra
- Bảng dữ liệu gồm: thời gian, loại (vào/ra), số tiền ETH, phí, số dư lũy kế.
- Một biểu đồ đường: trục ngang là thời gian, trục dọc là số dư lũy kế.
- Ba con số tổng hợp: tổng vào, tổng ra, số dư cuối kỳ.

## 5. Trường hợp ngoại lệ
- Nếu API trả về danh sách rỗng: in thông báo "Vi khong co giao dich trong ky", không báo lỗi.
- Nếu API trả về mã lỗi: in mã lỗi và dừng, không xử lý tiếp.
- Nếu ví có hơn 10.000 giao dịch: API trả theo trang, phải lấy đủ các trang.

## 6. Ngoài phạm vi
- Không phân tích giao dịch token (chỉ ETH gốc).
- Không quy đổi ra tiền Việt.