# BẰNG CHỨNG NỘP BÀI THỰC HÀNH - LAB 2

**Môn học:** Kinh tế số / Web3 Starter  
**Chủ đề:** LAB 2 — Ví và Giao dịch Đầu Tiên  
**Thời lượng:** 75 phút · Hình thức: Cặp đôi  

---

## 1. Thông tin chung
- **Họ và tên:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân (Ví gửi - Sinh viên):** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`
- **Địa chỉ ví bạn ghép cặp (Ví nhận - Bạn cùng thực hành):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Mạng thử nghiệm (Network):** Ethereum Sepolia Testnet

---

## 2. Bảng đối chiếu giao dịch (Giao dịch thành công & Giao dịch thất bại)

| Trường | Giao dịch thành công (Bước 1) | Giao dịch thất bại (Bước 2) |
| :--- | :--- | :--- |
| **Mã băm giao dịch (Tx Hash)** | [`0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3`](https://sepolia.etherscan.io/tx/0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3) | [`0x21916a7ed947234caffd6fac19105cfa9ca7d6dcbe309c0d7d2419a34277cde7`](https://sepolia.etherscan.io/tx/0x21916a7ed947234caffd6fac19105cfa9ca7d6dcbe309c0d7d2419a34277cde7) |
| **Số tiền chuyển** | `0.01 Sepolia ETH` *(hoặc chuyển thử nghiệm nội bộ cặp ví)* | `1.0 Sepolia ETH` *(Thử nghiệm chuyển không chừa đủ gas / lỗi hợp đồng)* |
| **Phí giao dịch thực trả** | `0.00005393 ETH` (21,000 Gas × 2.568 Gwei) | `0.00005336 ETH` (21,228 Gas × 2.513 Gwei) |
| **Trạng thái** | **Confirmed** (Thành công / Success) | **Failed / Reverted** (Thất bại trên chuỗi) |
| **Nguyên nhân (nếu thất bại)** | *Không có* (Giao dịch hợp lệ, trạng thái chuyển từ Pending sang Confirmed thành công). | Giao dịch bị revert/thất bại trong quá trình thực thi trên blockchain Sepolia. Dù thất bại, tài nguyên mạng vẫn tiêu tốn nên người gửi vẫn phải trả phí gas `0.00005336 ETH`. |

---

## 3. Phân tích chi tiết quá trình thực hành

### Bước 1 — Giao dịch thành công
- **Quy trình:** Ghép cặp hai sinh viên ngồi cạnh nhau, sao chép và đối chiếu địa chỉ ví `0x82d022a704706B2f144863D619D7418F8a0f19A7`.
- Thực hiện chuyển khoản trên MetaMask mạng Sepolia.
- Trạng thái giao dịch được theo dõi trực tiếp từ **Pending** (chờ xác thực trong mempool) sang **Confirmed** (đã được validator đóng gói vào block).
- Mã băm giao dịch (Transaction Hash) được ghi nhận thành công và hiển thị minh bạch trên Sepolia Etherscan Explorer.

---

### Bước 2 — Giao dịch thất bại có chủ đích (Phân tích 2 tình huống)

#### Tình huống A — Địa chỉ sai (Sai mã kiểm tra Checksum EIP-55):
- **Thử nghiệm:** Thay đổi 1 ký tự trong địa chỉ ví người nhận (ví dụ thay đổi chữ hoa/chữ thường hoặc ký tự hex).
- **Kết quả:** MetaMask phát hiện lỗi ngay tại giao diện người dùng (Client-side validation) và hiển thị cảnh báo *"Invalid recipient address"* hoặc sai checksum, vô hiệu hóa nút gửi. Giao dịch không thể phát sóng (broadcast) lên blockchain nên không sinh ra mã băm và không mất phí gas.
- **Bài học rút ra:** Địa chỉ ví Ethereum có cơ chế tự kiểm tra lỗi gõ nhầm (EIP-55 checksum), nhưng **hoàn toàn không thể kiểm tra được địa chỉ đó có thuộc về đúng người nhận mà bạn muốn gửi hay không**.

#### Tình huống B — Không đủ phí hoặc giao dịch thất bại trên chuỗi (On-chain Failure):
- **Thử nghiệm:** Gửi giao dịch toàn bộ số dư không chừa phí gas, hoặc điều chỉnh giới hạn gas / tương tác không đủ điều kiện khiến giao dịch bị revert on-chain (Mã băm: `0x21916a7ed947234caffd6fac19105cfa9ca7d6dcbe309c0d7d2419a34277cde7`).
- **Kết quả:** Giao dịch được đẩy lên mạng lưới nhưng không thể hoàn tất (Failed/Reverted). Mặc dù số tiền chuyển không bị trừ, tài khoản người gửi **vẫn bị trừ phí giao dịch (0.00005336 ETH)**.
- **Bài học rút ra:** Phí gas luôn phải được trả bằng đồng tiền gốc của mạng (ETH) để bồi hoàn cho năng lực tính toán của mạng lưới (validators), phí gas không được trừ vào số tiền chuyển và không được hoàn lại khi giao dịch thất bại.

---

## 4. Đoạn trả lời câu hỏi lý thuyết (3 câu)

> **Câu hỏi:** *Nếu bạn chuyển nhầm cho người lạ, có lấy lại được không? Vì sao?*

1. Nếu chuyển nhầm tài sản số cho người lạ trên mạng lưới blockchain, bạn **hoàn toàn không thể tự ý lấy lại** số tiền đó.  
2. Nguyên nhân là do bản chất của blockchain mang tính **bất biến (immutability)** và **phi tập trung (decentralization)**, không tồn tại cơ quan trung gian hay bên thứ ba nào (như ngân hàng hay tổ chức phát hành) có quyền hạn can thiệp để đảo ngược (reverse) hoặc hủy bỏ giao dịch đã được xác nhận.  
3. Bạn chỉ có thể nhận lại tài sản khi người nhận vô danh có thiện chí tự nguyện chuyển trả lại, bởi vì chỉ người nắm giữ **khóa riêng tư (private key)** của địa chỉ ví đó mới có quyền quyết định và ký giao dịch chuyển tiền ra khỏi ví.

---

## 5. Giá trị bài học gắn với công việc thực tế
- **Đối với chuyên viên tuân thủ (Compliance) & Kế toán tài sản số:** Cần phải nắm vững cấu trúc giao dịch (Nonce, Gas Limit, Gas Price, Base Fee, Data payload) và hiểu rõ nguyên nhân lỗi (Execution Reverted, Out of Gas, Nonce Mismatch, Checksum Failure).
- **Quy trình kiểm soát rủi ro:** Luôn yêu cầu quy trình xác thực địa chỉ ví hai bước (thử nghiệm gửi số tiền nhỏ test transfer trước khi chuyển khoản giá trị lớn) và kiểm toán hóa đơn phí gas cho các giao dịch on-chain của doanh nghiệp.

---

## 6. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao thuc hanh lab 2 - vi va giao dich dau tien"
git push
```
