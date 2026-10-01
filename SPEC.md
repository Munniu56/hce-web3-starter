# SPEC — CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ETHEREUM

## 1. Mục đích
Hệ thống này nhận vào một địa chỉ ví Ethereum bất kỳ, tự động trích xuất lịch sử giao dịch và phân tích báo cáo dòng tiền vào/ra trong 90 ngày gần nhất kèm biểu đồ trực quan hóa biến động số dư theo thời gian phục vụ chuyên viên phân tích nghiệp vụ (BA), kiểm soát tuân thủ (AML/KYC) và kế toán tài sản số.

## 2. Đầu vào
- Một địa chỉ ví Ethereum, dạng chuỗi ký tự 42 ký tự bắt đầu bằng tiền tố `0x`.
- Khóa API của Etherscan, đọc từ biến môi trường `ETHERSCAN_API_KEY`.
- Số ngày cần phân tích tính ngược từ thời điểm hiện tại, mặc định là `90` ngày.

## 3. Quy tắc nghiệp vụ
- **R1:** Giao dịch có trường `to` trùng khớp với địa chỉ đang xét và có trạng thái thành công (`isError == "0"`) được tính là dòng tiền vào.
- **R2:** Giao dịch có trường `from` trùng khớp với địa chỉ đang xét được tính là dòng tiền ra.
- **R3:** Với giao dịch đi ra có trạng thái thành công (`isError == "0"`), số tiền thực trừ khỏi số dư ví bằng: $\text{Giá trị chuyển (value)} + \text{Phí giao dịch (gasUsed} \times \text{gasPrice)}$.
- **R4:** Giao dịch do ví gửi đi có trạng thái thất bại (`isError == "1"`) vẫn bị trừ phí gas, khoản phí này bắt buộc phải tính vào dòng tiền ra; giá trị chuyển không bị trừ. Giao dịch người khác gửi đến ví bị lỗi thì không ghi nhận biến động và không chịu phí.
- **R5:** Mọi số tiền và phí gas lấy về từ API đều ở đơn vị số nguyên `wei`, bắt buộc phải chia cho $10^{18}$ trước khi tính toán lũy kế và hiển thị sang đơn vị `ETH`.
- **R6:** Sắp xếp toàn bộ danh sách giao dịch theo thời gian (`timeStamp`) tăng dần (từ quá khứ đến hiện tại) trước khi tính toán số dư lũy kế qua từng giao dịch.
- **R7 (Tự chuyển - Self-transfer):** Nếu giao dịch có `from == to`, giá trị chuyển không làm thay đổi số dư ròng, chỉ ghi nhận dòng tiền ra bằng đúng phí giao dịch ($\text{Transaction Fee}$).
- **R8 (Số dư khởi điểm):** Số dư đầu kỳ (90 ngày trước) = Số dư hiện tại từ API (`account.balance`) trừ đi tổng dòng tiền ròng trong kỳ ($\Delta = \text{Tổng vào} - \text{Tổng ra}$).

## 4. Đầu ra
- Bảng dữ liệu dòng tiền chi tiết gồm các cột: thời gian (`YYYY-MM-DD HH:mm:ss UTC`), mã băm giao dịch, phân loại (VÀO/RA), số tiền ETH, phí giao dịch ETH, số dư lũy kế ETH.
- Một biểu đồ đường: trục ngang (X) là thời gian, trục dọc (Y) là số dư ETH lũy kế.
- Ba con số tổng hợp: Tổng tiền vào (Total Inflow), Tổng tiền ra (Total Outflow), Số dư cuối kỳ (Closing Balance).

## 5. Trường hợp ngoại lệ
- Nếu API trả về danh sách rỗng: in thông báo `"Vi khong co giao dich trong ky"`, dừng xử lý và không báo lỗi.
- Nếu API trả về mã lỗi (`NOTOK`, `Invalid API Key`, `Rate limit`): in mã lỗi chi tiết và dừng, không xử lý tiếp.
- Nếu ví có hơn 10.000 giao dịch: thực hiện phân trang tự động (`page`, `offset`) để lấy đủ toàn bộ các trang dữ liệu, không bỏ sót.
- Nếu địa chỉ ví không hợp lệ (sai độ dài, không bắt đầu bằng `0x`, sai hex): báo lỗi định dạng ngay tại tầng kiểm tra đầu vào trước khi gọi API.

## 6. Ngoài phạm vi
- Không phân tích giao dịch token (chỉ phân tích đồng tiền cơ sở ETH gốc).
- Không quy đổi ra tiền pháp định (USD, VNĐ).
- Không phân tích các luồng giao dịch nội bộ sâu của hợp đồng thông minh phức tạp (Internal Trace).