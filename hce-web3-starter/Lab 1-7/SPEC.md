# SPEC — CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ON-CHAIN (LAB 5)

## 1. Mục đích
Hệ thống này giải quyết việc tự động trích xuất lịch sử giao dịch và phân tích dòng tiền vào/ra (Inflow/Outflow) trong 90 ngày gần nhất của một địa chỉ ví Ethereum, trực quan hóa biến động số dư theo thời gian phục vụ chuyên viên tuân thủ (AML/KYC) và kế toán tài sản số.

---

## 2. Đầu vào
- `address`: Chuỗi ký tự (String) độ dài 42 ký tự bắt đầu bằng tiền tố `0x`, đại diện cho địa chỉ ví hợp lệ trên mạng Ethereum (do người dùng cung cấp qua dòng lệnh hoặc giao diện).
- `ETHERSCAN_API_KEY`: Chuỗi ký tự khóa API Etherscan hợp lệ, được đọc tự động từ biến môi trường của hệ điều hành nhằm đảm bảo an toàn bảo mật (không ghi trực tiếp trong mã nguồn).
- `days`: Số nguyên (Integer) xác định khoảng thời gian phân tích tính ngược từ thời điểm hiện tại, giá trị mặc định là `90` ngày.

---

## 3. Quy tắc nghiệp vụ

- **R1 (Dòng tiền vào - Inflow):** Giao dịch có trường `to` trùng khớp với địa chỉ ví đang xét (không phân biệt chữ hoa/thường theo chuẩn EIP-55) và trạng thái thành công (`isError == "0"`) được tính là dòng tiền vào. Giá trị ghi nhận bằng đúng trường `value`.
- **R2 (Dòng tiền ra - Outflow):** Giao dịch có trường `from` trùng khớp với địa chỉ ví đang xét được tính là dòng tiền ra.
- **R3 (Số tiền thực trừ khi gửi thành công):** Với giao dịch đi ra có trạng thái thành công (`isError == "0"`), số tiền thực trừ khỏi số dư ví bằng tổng giá trị chuyển và chi phí giao dịch:
  $$\text{Số tiền trừ} = \text{Value} + \text{Transaction Fee} = \text{Value} + (\text{gasUsed} \times \text{gasPrice})$$
- **R4 (Xử lý giao dịch thất bại):** Giao dịch do ví gửi đi (`from == address`) có trạng thái thất bại (`isError == "1"`): Giá trị chuyển `value` không bị trừ (vì đã được EVM hoàn lại), nhưng **phí giao dịch vẫn bị trừ** khỏi ví. Khoản phí này bắt buộc phải được tính vào dòng tiền ra. Giao dịch người khác gửi đến ví (`to == address`) mà bị thất bại thì ví đang xét không ghi nhận biến động số dư và không chịu phí.
- **R5 (Quy đổi đơn vị chuẩn):** Mọi dữ liệu số tiền và phí gas lấy về từ Etherscan API đều ở đơn vị số nguyên nhỏ nhất `wei`. Bắt buộc phải quy đổi sang đơn vị `ETH` bằng cách chia cho $10^{18}$ trước khi tính toán lũy kế và hiển thị.
- **R6 (Chuẩn hóa thứ tự thời gian):** Toàn bộ danh sách giao dịch phải được sắp xếp theo thời gian (`timeStamp`) tăng dần (từ quá khứ đến hiện tại) trước khi tính toán số dư lũy kế qua từng giao dịch.
- **R7 (Quy tắc bổ sung — Giao dịch tự chuyển cho chính mình - Self-transfer):** Nếu giao dịch có `from == to` (người dùng tự chuyển ETH sang chính ví của mình): Giá trị chuyển `value` không làm biến động số dư ròng, nhưng ví bị trừ chi phí gas. Do đó, giao dịch này được ghi nhận vào dòng tiền ra với giá trị bằng đúng chi phí giao dịch ($\text{Transaction Fee}$).
- **R8 (Quy tắc bổ sung — Xác định số dư khởi điểm của kỳ phân tích):** Để số dư lũy kế trên biểu đồ phản ánh đúng số dư thực tế trong ví (không bị âm số dư giả lập khi ví có lệnh rút tiền ở đầu kỳ): Số dư đầu kỳ (90 ngày trước) được xác định bằng: lấy số dư hiện tại của ví (truy vấn qua API `account.balance`) trừ đi tổng dòng tiền ròng ($\Delta = \text{Tổng vào} - \text{Tổng ra}$) phát sinh trong 90 ngày đó.

---

## 4. Đầu ra

- **Bảng dữ liệu dòng tiền chi tiết (Data Table):** Hiển thị danh sách giao dịch gồm các cột:
  1. *Thời gian (Timestamp):* Định dạng ngày giờ `YYYY-MM-DD HH:mm:ss UTC`.
  2. *Mã băm giao dịch (Tx Hash):* Chuỗi rút gọn kèm liên kết Etherscan.
  3. *Phân loại dòng tiền:* `VÀO` (Inflow) hoặc `RA` (Outflow).
  4. *Số tiền chuyển (ETH):* Giá trị chuyển dịch.
  5. *Phí giao dịch (ETH):* Chi phí mạng lưới đã tiêu hao.
  6. *Số dư lũy kế (ETH):* Số dư tức thời của ví sau khi giao dịch hoàn tất.
- **Biểu đồ đường trực quan hóa (Balance Trend Chart):**
  - Trục hoành (X): Mốc thời gian diễn ra giao dịch.
  - Trục tung (Y): Số dư ETH lũy kế của ví tại từng thời điểm.
- **Thẻ tóm tắt 3 chỉ số kinh tế tổng hợp (Summary Metrics):**
  - **Tổng tiền vào (Total Inflow):** Tổng lượng ETH nạp vào ví trong kỳ (ETH).
  - **Tổng tiền ra (Total Outflow):** Tổng lượng ETH chuyển đi + tổng chi phí gas đã trả (ETH).
  - **Số dư cuối kỳ (Closing Balance):** Số dư tức thời của ví tại thời điểm báo cáo (ETH).

---

## 5. Trường hợp ngoại lệ

- **E1 (Ví không có giao dịch):** Nếu API trả về danh sách giao dịch rỗng (`result == []` hoặc thông báo *"No transactions found"*): Hệ thống in thông báo rõ ràng `"Vi khong co giao dich trong ky"` và dừng xử lý nhẹ nhàng, không gây sập chương trình.
- **E2 (Lỗi kết nối / Khóa API không hợp lệ):** Nếu API Etherscan trả về mã lỗi (như mã phản hồi `NOTOK`, lỗi xác thực `Invalid API Key`, hoặc bị chặn giới hạn tần suất `Max rate limit reached`): In thông báo lỗi chi tiết cùng mã lỗi và dừng chương trình.
- **E3 (Ví có số lượng giao dịch lớn > 10,000 giao dịch):** Cổng API Etherscan giới hạn tối đa 10,000 bản ghi trên mỗi lượt truy vấn. Nếu số lượng giao dịch vượt ngưỡng này, chương trình phải thực hiện phân trang tự động (`page`, `offset`) hoặc sử dụng khoảng block (`startblock`, `endblock`) để lấy đầy đủ toàn bộ dữ liệu, không được bỏ sót.
- **E4 (Định dạng địa chỉ ví không hợp lệ):** Nếu chuỗi nhập vào không đủ 42 ký tự, không bắt đầu bằng `0x` hoặc chứa ký tự không thuộc bảng mã thập lục phân (hexadecimal): Hệ thống báo lỗi `"Dia chi vi khong dung dinh dang Ethereum (EIP-55)"` ngay tại tầng kiểm tra đầu vào trước khi gọi API.

---

## 6. Ngoài phạm vi

- Bài lab này **KHÔNG** phân tích các giao dịch chuyển token ERC-20, NFT (ERC-721, ERC-1155) mà chỉ tập trung duy nhất vào đồng tiền cơ sở **ETH gốc**.
- **KHÔNG** xử lý việc quy đổi tỷ giá sang tiền pháp định (USD, VNĐ) trong khuôn khổ bài đặc tả này.
- **KHÔNG** phân tích các luồng giao dịch nội bộ sâu của hợp đồng phức tạp (Internal Trace) nếu không có yêu cầu mở rộng.
