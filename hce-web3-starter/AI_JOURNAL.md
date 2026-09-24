# NHẬT KÝ LÀM VIỆC VỚI AI - [Tên bài]

## Lần 1

**Prompt:** Viết hợp đồng Solidity [TênHợpĐồng] với các hàm xử lý dữ liệu [TênHàm].

**AI trả về:** Sinh mã nguồn hợp đồng cơ bản thực hiện ghi nhận dữ liệu nhưng chưa kiểm tra phân quyền và không có sự kiện[cite: 11].

**Đánh giá:** Phải sửa

**Chỗ sai:** 
1. Dòng [Số dòng, ví dụ: 15]: Hàm `public` thiếu kiểm tra phân quyền `onlyOwner`, cho phép bất kỳ ví nào cũng thực thi được[cite: 11].
2. Dòng [Số dòng, ví dụ: 22]: Thay đổi trạng thái storage nhưng không phát ra `event`, vi phạm quy ước `AGENTS.md`[cite: 11].

**Cách sửa:** Sinh viên tự thêm `modifier onlyOwner` vào hàm và khai báo/gọi `emit [TênEvent]()` để ghi nhận sự kiện[cite: 11].

**Ai phát hiện:** Sinh viên phát hiện