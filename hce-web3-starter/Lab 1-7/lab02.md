# BẰNG CHỨNG NỘP BÀI THỰC HÀNH - LAB 2

**Môn học:** TDT&HDTM / Web3 Starter  
**Chủ đề:** LAB 2 — Ví và Giao dịch Đầu Tiên  
**Thời lượng:** 75 phút · **Hình thức:** Cặp đôi  

---

## 1. Thông tin chung
- **Họ và tên:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân (Ví gửi - Sinh viên):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Địa chỉ ví bạn ghép cặp (Ví nhận - Bạn cùng thực hành):** `0x36Fd4887e9d1ecA4Ae5062A745cc2c6182B77060`
- **Mạng thử nghiệm (Network):** Ethereum Sepolia Testnet

---

## 2. Bảng đối chiếu giao dịch (Giao dịch thành công & Giao dịch thất bại)

| Trường | Giao dịch thành công (Bước 1) | Giao dịch thất bại (Bước 2) |
| :--- | :--- | :--- |
| **Mã băm giao dịch (Tx Hash)** | [`0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d`](https://sepolia.etherscan.io/tx/0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d) | [`0xf4351a9b2898255a8c945a569875b74b52c8a7e8ef4e72a5f298942e3f80d3e9`](https://sepolia.etherscan.io/tx/0xf4351a9b2898255a8c945a569875b74b52c8a7e8ef4e72a5f298942e3f80d3e9) |
| **Số tiền chuyển** | `2.0 Sepolia ETH` *(giao dịch chuyển trực tiếp sang ví bạn ghép cặp; định mức chuẩn: `0.01 Sepolia ETH`)* | `0.0 Sepolia ETH` *(thử nghiệm gọi giao dịch bị Revert / không đủ điều kiện thực thi trên chuỗi)* |
| **Phí giao dịch thực trả** | `0.00005222 ETH` (21,000 Gas × 2.487 Gwei) | `0.00006615 ETH` (25,892 Gas × 2.555 Gwei) |
| **Trạng thái** | **Confirmed** (Thành công / Success) | **Failed / Reverted** (Thất bại trên chuỗi) |
| **Nguyên nhân (nếu thất bại)** | *Không có* (Giao dịch hợp lệ, trạng thái chuyển từ Pending sang Confirmed thành công trên Block #11673318). | Giao dịch bị revert do vi phạm điều kiện thực thi trên blockchain Sepolia. Mặc dù số tiền chuyển không bị trừ, tài khoản người gửi vẫn bị tiêu tốn tài nguyên mạng và phải trả phí gas thực tế `0.00006615 ETH`. |

> **Ghi chú mở rộng (Đối chiếu liên kết giữa cặp ví):**
> - Bạn ghép cặp cũng đã gửi đối ứng thành công sang ví sinh viên với các mã băm: [`0x9277e9bae8aad5297cd710ff3e7552a5706b0e1a0c78203376e73957b6948821`](https://sepolia.etherscan.io/tx/0x9277e9bae8aad5297cd710ff3e7552a5706b0e1a0c78203376e73957b6948821) (`0.1 ETH`) và [`0x9558ebed34c4c88520ba7d8aa9c782a153b50a618da48c4030fa8235f0c88be7`](https://sepolia.etherscan.io/tx/0x9558ebed34c4c88520ba7d8aa9c782a153b50a618da48c4030fa8235f0c88be7) (`0.11 ETH`).
> - Mã băm thử nghiệm thất bại do cạn kiệt gas / lỗi on-chain khác: [`0x21916a7ed947234caffd6fac19105cfa9ca7d6dcbe309c0d7d2419a34277cde7`](https://sepolia.etherscan.io/tx/0x21916a7ed947234caffd6fac19105cfa9ca7d6dcbe309c0d7d2419a34277cde7) (Phí gas: `0.00005336 ETH`).

---

## 3. Phân tích chi tiết quá trình thực hành

### Bước 1 — Giao dịch thành công
1. **Ghép cặp & Thiết lập:** Hai sinh viên ngồi cạnh nhau tiến hành trao đổi và đối chiếu địa chỉ ví công khai:
   - Ví gửi (Sinh viên Ngô Thị Thúy Vân): `0x82d022a704706B2f144863D619D7418F8a0f19A7`
   - Ví nhận (Bạn cùng thực hành): `0x36Fd4887e9d1ecA4Ae5062A745cc2c6182B77060`
2. **Khởi tạo giao dịch:** Nhập địa chỉ ví bạn nhận vào MetaMask trên mạng Sepolia Testnet, chỉ định số tiền cần chuyển.
3. **Theo dõi vòng đời giao dịch:**
   - Khi ký và gửi, giao dịch đầu tiên đi vào trạng thái **Pending** (nằm trong Mempool - hàng đợi chờ xác nhận của mạng lưới Ethereum Sepolia).
   - Sau đó validator chọn giao dịch, đóng gói vào Block `#11673318` và chuyển sang trạng thái **Confirmed**.
4. **Ghi nhận mã băm:** Thu được Tx Hash [`0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d`](https://sepolia.etherscan.io/tx/0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d), tra cứu hiển thị đầy đủ và minh bạch trên Sepolia Etherscan Explorer.

---

### Bước 2 — Giao dịch thất bại có chủ đích (Phân tích 2 tình huống)

#### Tình huống A — Địa chỉ sai (Sai mã kiểm tra Checksum EIP-55):
- **Thử nghiệm:** Thay đổi 1 ký tự bất kỳ trong địa chỉ ví người nhận `0x36Fd4887e9d1ecA4Ae5062A745cc2c6182B77060` (ví dụ sửa thành `0x36Fe4887e9d1ecA4Ae5062A745cc2c6182B77060` hoặc thay đổi quy tắc chữ hoa/chữ thường làm sai lệch mã băm Keccak-256).
- **Kết quả:** MetaMask nhận diện lỗi ngay tại phía giao diện người dùng (Client-side validation) và hiển thị thông báo lỗi *"Invalid recipient address"*, đồng thời khóa nút xác nhận gửi. Giao dịch bị chặn trước khi được broadcast lên mạng lưới blockchain, do đó không tạo ra mã băm (Tx Hash) và không tiêu tốn phí gas.
- **Bài học rút ra:** Địa chỉ ví Ethereum có cơ chế tự kiểm tra lỗi gõ nhầm (EIP-55 checksum), nhưng **hoàn toàn không thể kiểm tra được địa chỉ đó có thuộc về đúng người nhận mà bạn dự định gửi hay không** (nếu người gửi nhập nhầm một địa chỉ ví hợp lệ khác của người lạ, hệ thống vẫn chấp nhận chuyển tiền đi bình thường).

#### Tình huống B — Không đủ phí hoặc giao dịch thất bại trên chuỗi (On-chain Failure / Execution Reverted):
- **Thử nghiệm:** Thử chuyển toàn bộ số dư trong ví mà không chừa lại ETH để thanh toán phí gas, hoặc cố tình gửi giao dịch gọi hàm hợp đồng vi phạm điều kiện thực thi khiến giao dịch bị revert on-chain (Mã băm: `0xf4351a9b2898255a8c945a569875b74b52c8a7e8ef4e72a5f298942e3f80d3e9`).
- **Kết quả:** Giao dịch được phát sóng lên blockchain, tuy nhiên trong quá trình thực thi trên máy ảo EVM, điều kiện hợp lệ không được thỏa mãn dẫn đến trạng thái **Failed / Reverted**. Dù số tiền chuyển không bị trừ khỏi ví gửi, tài khoản người gửi **vẫn bị trừ toàn bộ phí giao dịch thực tế (`0.00006615 ETH`)**.
- **Bài học rút ra:** Phí giao dịch (gas) luôn phải được thanh toán bằng đồng tiền gốc của mạng lưới (Sepolia ETH) để bù đắp năng lực tính toán cho các validator, phí gas không được trừ vào số tiền chuyển và hoàn toàn không được hoàn lại kể cả khi giao dịch bị thất bại.

---

## 4. Đoạn trả lời câu hỏi lý thuyết (Đúng 3 câu)

> **Câu hỏi:** *Nếu bạn chuyển nhầm cho người lạ, có lấy lại được không? Vì sao?*

1. Nếu bạn chuyển nhầm tài sản số cho người lạ trên blockchain, bạn **hoàn toàn không thể tự ý lấy lại** số tiền đó.  
2. Nguyên nhân là do bản chất của mạng lưới blockchain hoạt động theo nguyên tắc **bất biến (immutability)** và **phi tập trung (decentralization)**, không tồn tại cơ quan trung gian hay bên thứ ba nào (như ngân hàng hay tổ chức phát hành) có thẩm quyền can thiệp để hủy bỏ hoặc đảo ngược (reverse) một giao dịch đã được xác nhận vào khối.  
3. Bạn chỉ có thể nhận lại tài sản nếu người nhận lạ có thiện chí tự nguyện chuyển trả lại, bởi vì chỉ duy nhất người nắm giữ **khóa riêng tư (private key)** của địa chỉ nhận đó mới có quyền hạn hợp pháp để ký duyệt và chuyển tài sản ra khỏi ví.

---

## 5. Giá trị bài học gắn với công việc thực tế
- **Đối với chuyên viên tuân thủ (Compliance) & Kế toán tài sản số:** Cần phải hiểu rõ cấu trúc giao dịch (Nonce, Gas Limit, Gas Price, Base Fee, Priority Fee, Data Payload) và nắm vững cách phân loại các lỗi phát sinh (Client Checksum Error vs. Execution Reverted, Out of Gas).
- **Hạch toán chi phí:** Các giao dịch thất bại on-chain vẫn phải được hạch toán chi phí gas hợp lệ vào sổ sách kế toán vì phí này đã thực chi trên blockchain và không thể thu hồi.
- **Quy trình kiểm soát rủi ro:** Trong môi trường doanh nghiệp Web3, nhân sự tài chính phải luôn áp dụng quy trình chuyển thử nghiệm một số tiền nhỏ (*test transaction*) trước khi giải ngân các giao dịch giá trị lớn, đồng thời triển khai cơ chế danh sách trắng (*whitelisting*) cho các địa chỉ ví đối tác.

---

## 6. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao thuc hanh lab 2 - vi va giao dich dau tien"
git push
```
