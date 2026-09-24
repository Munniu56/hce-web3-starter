# SPEC – [Tên bài Lab / Tên Hợp đồng]

## 1. Mục đích
Hệ thống này giải quyết việc [mô tả ngắn gọn chức năng: lưu trữ/xác thực/chuyển tiền...] cho [đối tượng sử dụng: Người dùng/Admin][cite: 16].

## 2. Đầu vào
- `[tên_tham_số_1]`: [Kiểu dữ liệu: uint256/string/address/bytes32], do [Người dùng/Admin] cung cấp[cite: 16].
- `[tên_tham_số_2]`: [Kiểu dữ liệu: uint256/string/address/bytes32], do [Người dùng/Admin] cung cấp[cite: 16].

## 3. Quy tắc nghiệp vụ
- R1: [Mô tả quy tắc chính 1 từ đề bài, ví dụ: Chỉ Owner mới có quyền gọi hàm][cite: 12, 16].
- R2: [Mô tả quy tắc chính 2 từ đề bài, ví dụ: Tham số đầu vào không được để rỗng hoặc bằng 0][cite: 16].
- R3 (Bổ sung nâng cao 1): Mỗi dữ liệu/địa chỉ ví chỉ được ghi nhận đúng 1 lần, không cho phép ghi đè để bảo đảm tính toàn vẹn[cite: 16].
- R4 (Bổ sung nâng cao 2): Mọi hàm làm thay đổi trạng thái bắt buộc phải phát ra sự kiện (`event`) tương ứng theo quy ước[cite: 11, 16].

## 4. Đầu ra
- Kết quả [tên dữ liệu/trạng thái], được lưu cố định trên blockchain và hiển thị tại [màn hình/console/hàm tra cứu][cite: 16].

## 5. Trường hợp ngoại lệ
- Nếu tài khoản không phải Owner cố tình gọi hàm thì hệ thống phải dừng giao dịch và revert lỗi `NotOwner()`[cite: 12, 16].
- Nếu truyền tham số đầu vào rỗng (hoặc bằng 0) thì hệ thống phải revert lỗi `InvalidInput()`[cite: 16].
- Nếu thao tác trên dữ liệu đã tồn tại hoặc vi phạm R3, hệ thống phải revert lỗi `AlreadyExists()`[cite: 16].

## 6. Ngoài phạm vi
- Bài lab này không xử lý việc lưu trữ các tệp phương tiện kích thước lớn trực tiếp trên Smart Contract[cite: 16].