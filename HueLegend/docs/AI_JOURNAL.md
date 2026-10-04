# AI_JOURNAL — NHẬT KÝ SỬ DỤNG AI VÀ LỖI ĐÃ PHÁT HIỆN

Dự án: **HueLegend — Truy xuất nguồn gốc đặc sản Huế**  
Khung làm việc: ECO2432 / K57 Kinh tế số  
Công cụ trợ lý AI: **Antigravity IDE (Gemini 3.8 Flash)**

---

## 1. Phiên làm việc khởi tạo cấu trúc dự án (Lab 8)

### Mục tiêu phiên làm việc
Yêu cầu AI sinh cấu trúc chuẩn hóa cho đề tài **HueLegend** từ bản mẫu Lab 8, thiết kế hợp đồng thông minh `ProjectCore.sol` cho luồng cốt lõi:
$$\text{Tạo lô} \longrightarrow \text{Thêm chặng bởi đúng vai} \longrightarrow \text{Quét QR xem lịch sử}$$

### Mẫu câu lệnh (Prompt) đưa vào
> *"Tạo cấu trúc dự án chuẩn Lab 8 cho dự án HueLegend về Truy xuất đặc sản Huế. Giải quyết bài toán cơ sở và khách mua cần lịch sử lô hàng bất biến. Luồng cốt lõi demo: Tạo lô -> thêm chặng bởi đúng vai -> quét QR xem lịch sử. Tuân thủ tuyệt đối AGENTS.md (Solidity ^0.8.20, CEI, custom error, event, chú thích không dấu, tối thiểu 3 test case gồm ca gian lận)."*

---

## 2. Các lỗi thiết kế và bảo mật đã phát hiện & Cách khắc phục

### Lỗi 01: Nguy cơ mạo danh vai trò khi ghi nhận chặng (Role Impersonation)
- **Vấn đề phát hiện ban đầu:** Trong bản phác thảo đầu tiên, hàm `addCheckpoint` chỉ nhận tham số `string roleName` mà không kiểm tra xem địa chỉ ví `msg.sender` có thực sự được cấp quyền hay không.
- **Rủi ro:** Một địa chỉ ví bất kỳ (kẻ xấu / cửa hàng bán hàng giả) có thể tự xưng là `"CO_SO_SAN_XUAT"` hoặc `"KIEM_DINH_OCOP"` để ghi chặng giả mạo vào lô hàng.
- **Cách khắc phục:**
  - Chuyển sang định danh vai trò bằng hằng số hàm băm `bytes32`: `ROLE_PRODUCER`, `ROLE_LOGISTICS`, `ROLE_RETAILER`, `ROLE_INSPECTOR`.
  - Sử dụng bảng ánh xạ phân quyền `mapping(address => mapping(bytes32 => bool)) private _roles;`.
  - Trong hàm `addCheckpoint`, bắt buộc kiểm tra `if (!_roles[msg.sender][role] && msg.sender != owner()) revert UnauthorizedCaller(msg.sender, role);`.

### Lỗi 02: Lãng phí chi phí Gas do dùng chuỗi thông báo lỗi dài
- **Vấn đề phát hiện:** Khi kiểm tra điều kiện dữ liệu đầu vào, việc dùng `require(bytes(batchCode).length > 0, "Ma lo hang khong duoc de trong")` gây tốn thêm mã bytecode triển khai và chi phí gas khi thực thi.
- **Cách khắc phục:** Chuyển đổi toàn bộ sang `Custom Errors` của Solidity `^0.8.20`:
  ```solidity
  error BatchAlreadyExists(string batchCode);
  error BatchNotFound(string batchCode);
  error UnauthorizedCaller(address caller, bytes32 requiredRole);
  error EmptyString(string paramName);
  ```
  Giúp giảm đáng kể gas triển khai và tương thích hoàn hảo với quy ước `AGENTS.md`.

### Lỗi 03: Nguy cơ cạn kiệt Gas khi đọc danh sách chặng (Unbounded Array DOS)
- **Vấn đề phát hiện:** Nếu một lô hàng có hàng chục chặng lưu kho và vận chuyển kéo dài, việc trả về mảng `Checkpoint[]` trong một giao dịch ghi trạng thái sẽ gây tốn gas đột biến.
- **Cách khắc phục:** Thiết kế hàm `getCheckpoints(string calldata batchCode)` là hàm `view` thuần túy. Khách hàng quét mã QR chỉ gọi RPC đọc ngoài chuỗi (off-chain eth_call), hoàn toàn không tốn gas và không bị ảnh hưởng bởi giới hạn block gas limit.

### Lỗi 04: Vi phạm quy ước ngôn ngữ chú thích trong mã nguồn
- **Vấn đề phát hiện:** Trợ lý AI ban đầu sinh chú thích bằng tiếng Việt có dấu (`// Kiểm tra quyền của cơ sở sản xuất`).
- **Quy tắc vi phạm:** Mục 4 trong `AGENTS.md` yêu cầu *"Chú thích trong mã viết bằng tiếng Việt không dấu"*.
- **Cách khắc phục:** Quét và chuẩn hóa toàn bộ chú thích trong hợp đồng `ProjectCore.sol` sang tiếng Việt không dấu (`// Kiem tra quyen cua co so san xuat`).

---

## 3. Đánh giá chất lượng và Thẩm định

- **Độ bao phủ kiểm thử:** Xây dựng đầy đủ 4 ca kiểm thử tại `test/ProjectCore.test.js`, trong đó có ca kiểm thử gian lận TC-03 nhằm chứng minh tính an toàn khi kẻ xấu cố tình chèn chặng giả mạo.
- **Tính khả thi của luồng demo:** Luồng 3 bước hoạt động trơn tru từ giao diện Web3 đến tầng hợp đồng thông minh.
