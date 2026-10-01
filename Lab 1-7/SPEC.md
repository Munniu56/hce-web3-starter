# BÁO CÁO THỰC HÀNH — LAB 5: VIẾT ĐẶC TẢ CHO CÔNG CỤ PHÂN TÍCH DÒNG TIỀN

**Môn học:** TDT&HDTM / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 5 — Viết đặc tả cho công cụ phân tích dòng tiền  
**Thời lượng:** 75 phút · **Hình thức:** Nhóm 2 người · **Quy tắc:** KHÔNG VIẾT MÃ NGUỒN TRONG BUỔI NÀY  
**Sản phẩm nộp:** `SPEC.md` + Nhận xét của nhóm bạn  

---

## 1. Thông tin chung
- **Họ và tên sinh viên thực hiện:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân (Ví sinh viên):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Địa chỉ ví bạn ghép cặp (Kiểm tra chéo / Peer Review):** `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`
- **Tệp đặc tả trong dự án:** [`Lab 1-7/SPEC.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/SPEC.md)

---

## 2. Bản đặc tả chi tiết (System Specification)

### 2.1. Mục đích
Hệ thống này nhận vào một địa chỉ ví Ethereum bất kỳ, tự động trích xuất lịch sử giao dịch và phân tích báo cáo dòng tiền vào/ra trong 90 ngày gần nhất kèm biểu đồ trực quan hóa biến động số dư theo thời gian phục vụ chuyên viên phân tích nghiệp vụ (BA), kiểm soát tuân thủ (AML/KYC) và kế toán tài sản số.

---

### 2.2. Đầu vào (Inputs)
- **`address`:** Một địa chỉ ví Ethereum, dạng chuỗi ký tự (String) 42 ký tự bắt đầu bằng tiền tố `0x` (không phân biệt chữ hoa/thường theo chuẩn EIP-55).
- **`ETHERSCAN_API_KEY`:** Khóa API của Etherscan, bắt buộc đọc từ biến môi trường hệ thống nhằm đảm bảo an toàn bảo mật, tuyệt đối không hardcode trong mã nguồn.
- **`days`:** Số ngày cần phân tích tính ngược từ thời điểm hiện tại, giá trị mặc định là `90` ngày.

---

### 2.3. Quy tắc nghiệp vụ (Business Rules)
- **R1 (Dòng tiền vào - Inflow):** Giao dịch có trường `to` trùng khớp với địa chỉ đang xét và có trạng thái thành công (`isError == "0"`) được tính là dòng tiền vào. Giá trị ghi nhận bằng đúng trường `value`.
- **R2 (Dòng tiền ra - Outflow):** Giao dịch có trường `from` trùng khớp với địa chỉ đang xét được tính là dòng tiền ra.
- **R3 (Số tiền thực trừ của giao dịch gửi đi thành công):** Với giao dịch đi ra có trạng thái thành công (`isError == "0"`), số tiền thực trừ khỏi số dư ví bằng tổng giá trị chuyển và phí giao dịch:
  $$\text{Số tiền thực trừ} = \text{Value} + \text{Transaction Fee} = \text{Value} + (\text{gasUsed} \times \text{gasPrice})$$
- **R4 (Xử lý giao dịch thất bại):** Giao dịch do ví gửi đi (`from == address`) có trạng thái thất bại (`isError == "1"`): Giá trị chuyển `value` không bị trừ (vì đã được EVM hoàn lại), nhưng **phí giao dịch vẫn bị trừ** khỏi ví. Khoản phí này bắt buộc phải được tính vào dòng tiền ra. Giao dịch người khác gửi đến ví (`to == address`) mà bị thất bại thì ví đang xét không ghi nhận biến động số dư và không chịu phí.
- **R5 (Quy đổi đơn vị chuẩn):** Mọi số tiền và phí gas lấy về từ Etherscan API đều ở đơn vị số nguyên nhỏ nhất `wei`. Bắt buộc phải chia cho $10^{18}$ trước khi tính toán lũy kế và hiển thị sang đơn vị `ETH`.
- **R6 (Sắp xếp theo thời gian):** Toàn bộ danh sách giao dịch phải được sắp xếp theo thời gian (`timeStamp`) tăng dần (từ quá khứ đến hiện tại) trước khi tính toán số dư lũy kế qua từng giao dịch.
- **R7 (Quy tắc bổ sung — Giao dịch tự chuyển cho chính mình - Self-transfer):** Nếu giao dịch có `from == to` (người dùng tự chuyển ETH sang chính ví của mình): Giá trị chuyển `value` không làm biến động số dư ròng, nhưng ví bị trừ chi phí gas. Do đó, giao dịch này được ghi nhận vào dòng tiền ra với giá trị bằng đúng chi phí giao dịch ($\text{Transaction Fee}$).
- **R8 (Quy tắc bổ sung — Xác định số dư khởi điểm của kỳ phân tích):** Để số dư lũy kế trên biểu đồ phản ánh đúng số dư thực tế trong ví (không bị âm số dư giả lập khi ví có lệnh rút tiền ở đầu kỳ): Số dư đầu kỳ (90 ngày trước) được xác định bằng: lấy số dư hiện tại của ví (truy vấn qua API `account.balance`) trừ đi tổng dòng tiền ròng ($\Delta = \text{Tổng vào} - \text{Tổng ra}$) phát sinh trong 90 ngày đó.

---

### 2.4. Đầu ra (Outputs)
- **Bảng dữ liệu dòng tiền chi tiết (Data Table):** Hiển thị danh sách giao dịch với đầy đủ các cột:
  1. *Thời gian (Timestamp):* Định dạng ngày giờ chuẩn `YYYY-MM-DD HH:mm:ss UTC`.
  2. *Mã băm giao dịch (Tx Hash):* Dạng rút gọn kèm liên kết tra cứu Etherscan.
  3. *Phân loại dòng tiền:* `VÀO` (Inflow) hoặc `RA` (Outflow).
  4. *Số tiền chuyển (ETH):* Lượng ETH luân chuyển của giao dịch.
  5. *Phí giao dịch (ETH):* Chi phí mạng lưới thực tế đã tiêu hao.
  6. *Số dư lũy kế (ETH):* Số dư tức thời của ví ngay sau khi giao dịch hoàn tất.
- **Một biểu đồ đường (Balance Trend Chart):**
  - Trục ngang (X): Mốc thời gian diễn ra giao dịch.
  - Trục dọc (Y): Số dư ETH lũy kế của ví tại từng thời điểm.
- **Ba con số tổng hợp (Summary Metrics):**
  - **Tổng tiền vào (Total Inflow):** Tổng lượng ETH nạp vào ví trong kỳ (ETH).
  - **Tổng tiền ra (Total Outflow):** Tổng lượng ETH chuyển đi + tổng chi phí gas đã trả (ETH).
  - **Số dư cuối kỳ (Closing Balance):** Số dư tức thời của ví tại thời điểm báo cáo (ETH).

---

### 2.5. Trường hợp ngoại lệ (Edge Cases & Exceptions)
- **E1 (API trả về danh sách rỗng):** Nếu API trả về danh sách rỗng (`result == []` hoặc thông báo *"No transactions found"*): In thông báo `"Vi khong co giao dich trong ky"` và dừng xử lý nhẹ nhàng, không báo lỗi và không làm sập chương trình.
- **E2 (API trả về mã lỗi):** Nếu API trả về mã lỗi (như mã phản hồi `NOTOK`, `Invalid API Key`, hoặc bị chạm giới hạn tần suất `Max rate limit reached`): In mã lỗi chi tiết và dừng chương trình, không xử lý tiếp.
- **E3 (Ví có hơn 10.000 giao dịch):** Cổng API Etherscan giới hạn tối đa 10,000 bản ghi trên mỗi lượt truy vấn. Nếu số lượng giao dịch vượt ngưỡng này, chương trình phải thực hiện phân trang tự động (`page`, `offset`) để lấy đầy đủ toàn bộ các trang dữ liệu, không được bỏ sót.
- **E4 (Địa chỉ ví sai định dạng):** Nếu chuỗi nhập vào không đủ 42 ký tự, không bắt đầu bằng `0x` hoặc chứa ký tự không thuộc bảng mã thập lục phân (hexadecimal): Báo lỗi `"Dia chi vi khong hop le theo chuan EIP-55"` ngay tại tầng kiểm tra dữ liệu đầu vào trước khi gọi API.

---

### 2.6. Ngoài phạm vi (Out of Scope)
- **Không phân tích giao dịch token:** Không phân tích token ERC-20 hay NFT (ERC-721, ERC-1155), chỉ tập trung duy nhất vào đồng tiền cơ sở **ETH gốc**.
- **Không quy đổi ra tiền Việt:** Không xử lý quy đổi tỷ giá sang tiền pháp định (USD, VNĐ) trong khuôn khổ bài đặc tả này.
- **Không phân tích luồng giao dịch nội bộ sâu (Internal Transactions):** Bỏ qua các lệnh gọi hợp đồng phức tạp nhiều tầng nếu không có yêu cầu mở rộng.

---

## 3. Bước 3 — Biên bản kiểm tra chéo & Nhận xét của nhóm bạn

Thực hiện đúng quy trình kiểm tra chéo (Peer Review) giữa hai nhóm trong 15 phút, chỉ ra các điểm mơ hồ theo yêu cầu của giáo trình:

| STT | Điểm phản biện từ nhóm bạn | Phân tích tính mơ hồ / Rủi ro phát sinh | Phản hồi & Giải pháp tiếp thu của nhóm tác giả |
| :---: | :--- | :--- | :--- |
| **1** | **Chưa nêu rõ hành vi khi người dùng tự chuyển cho chính mình (`from == to`)** | Nếu áp dụng máy móc quy tắc R1 (tính vào) và R2 (tính ra), giao dịch sẽ bị cộng giá trị chuyển `value` vào dòng tiền vào và đồng thời trừ đi ở dòng tiền ra $\rightarrow$ làm phình to doanh số luân chuyển ảo, dù thực tế số dư chỉ giảm một lượng bằng tiền phí gas. | **Đã tiếp thu và bổ sung quy tắc R7:** Giao dịch tự chuyển không làm thay đổi số dư về mặt giá trị gốc, chỉ ghi nhận dòng tiền ra bằng đúng khoản phí giao dịch ($\text{Transaction Fee}$). |
| **2** | **Cách tính mốc bắt đầu của số dư lũy kế (Initial Balance) chưa cụ thể** | Nếu số dư lũy kế bắt đầu từ mốc `0`, khi ví thực hiện lệnh chuyển tiền ngay giao dịch đầu kỳ thì số dư tức thời sẽ bị âm (ví dụ: `-0.5 ETH`). Điều này vi phạm nghiêm trọng nguyên lý kế toán và logic blockchain (số dư tài khoản không thể âm). | **Đã tiếp thu và bổ sung quy tắc R8:** Xác định số dư gốc đầu kỳ (90 ngày trước) bằng cách lấy số dư hiện tại từ API trừ đi tổng biến động ròng trong kỳ ($\Delta = \text{Inflow} - \text{Outflow}$), từ đó đường biểu diễn luôn dương và sát thực tế. |
| **3** | **Cần làm rõ trường hợp người khác gửi tiền đến ví nhưng giao dịch bị lỗi** | Đề bài gốc nêu "Giao dịch thất bại vẫn tính phí", nhưng chưa tách rõ vai trò: Ví nhận (`to == address`) có bị ảnh hưởng gì không nếu người gửi thực hiện lệnh thất bại? | **Đã làm rõ tại quy tắc R4:** Chỉ có người gửi (`from == address`) mới bị trừ phí mạng lưới khi giao dịch thất bại. Ví nhận hoàn toàn không bị ảnh hưởng và không ghi nhận biến động số dư. |
| **4** | **Cơ chế phân trang khi ví vượt quá 10.000 giao dịch** | Nếu chỉ gọi API mặc định một lần, các ví có tần suất hoạt động cao sẽ bị mất dữ liệu các giao dịch cũ hơn 10,000 bản ghi, dẫn đến báo cáo tài chính bị sai lệch nghiêm trọng. | **Đã tiếp thu tại ngoại lệ E3:** Thiết lập vòng lặp phân trang tự động (`page` tăng dần, `offset = 10000`) cho đến khi số bản ghi trả về nhỏ hơn `offset` để đảm bảo vét cạn toàn bộ dữ liệu. |

---

## 4. Giá trị bài học đối với vai trò Chuyên viên Phân tích Nghiệp vụ (BA)
- **Tầm quan trọng của việc "tách riêng buổi viết đặc tả, không gõ mã nguồn":** Khi không bị phân tâm bởi cú pháp lập trình, sinh viên tập trung 100% tư duy vào việc chuẩn hóa logic kinh tế, phòng ngừa các trường hợp biên (*edge cases*) và xử lý ngoại lệ.
- **Kỹ năng viết yêu cầu là kỹ năng "bán được cho nhà tuyển dụng":** Trong kỷ nguyên AI tạo sinh (GenAI), khả năng viết đặc tả kỹ thuật rành mạch, không mơ hồ quyết định chất lượng đầu ra của mã nguồn AI sinh ra ở Lab 6, giúp tiết kiệm thời gian gỡ lỗi và đảm bảo tính toán chuẩn xác cho các hệ thống tài chính Web3.

---

## 5. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs(lab-05): hoan thanh dac ta SPEC.md va bien ban kiem tra cheo lab 5"
git push
```
