# BÁO CÁO THỰC HÀNH — LAB 4: NHẬN DIỆN HỢP ĐỒNG CÓ RỦI RO

**Môn học:** Kinh tế số / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 4 — Nhận diện hợp đồng có rủi ro  
**Thời lượng:** 75 phút · **Hình thức:** Cá nhân / Nhóm 2 người  
**Sản phẩm nộp:** `lab04.md` + mục ghi trong `AI_JOURNAL.md`  

---

## 1. Thông tin chung
- **Họ và tên:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân:** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`
- **Tệp mã nguồn thẩm định:** [`contracts/lab04/ClubTokens.sol`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/contracts/lab04/ClubTokens.sol)

---

## 2. Bước 1 — Đọc thủ công trước mã nguồn hợp đồng (15 phút)

Trước khi dùng công cụ AI, sinh viên thực hiện đọc rà soát thủ công 40 dòng mã trong tệp `ClubTokens.sol` và ghi nhận sơ bộ:
- **`ClubTokenA` (Dòng 7–11):** Hợp đồng chỉ kế thừa `ERC20`, hàm khởi tạo `constructor` đúc 1,000,000 token cho `msg.sender`. Không có từ khóa `Ownable`, không có biến chủ sở hữu hay hàm quản trị nào.
- **`ClubTokenB` (Dòng 13–21):** Hợp đồng kế thừa `ERC20` và `Ownable`. Có một hàm ngoại vi `mint(address to, uint256 amount)` có gắn modifier `onlyOwner` ở dòng 18–20.
- **`ClubTokenC` (Dòng 23–38):** Hợp đồng kế thừa `ERC20` và `Ownable`. Có mapping `restricted` lưu trạng thái hạn chế của từng ví (dòng 24). Hàm `setRestricted` (dòng 30–32) cho phép `onlyOwner` bật/tắt cấm ví. Hàm `_update` (dòng 34–37) chặn các giao dịch chuyển tiền nếu ví gửi nằm trong danh sách cấm.

---

## 3. Bước 2 — Thẩm định bằng công cụ AI với vai trò chuyên viên rủi ro

Áp dụng đúng prompt chuẩn từ `prompt_templates.md`:

```text
Bạn là chuyên viên thẩm định rủi ro tài sản số.
Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà
chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
– Tên hàm và số dòng
– Người nắm giữ token chịu rủi ro gì
Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.

[Mã nguồn ClubTokens.sol]
```

---

## 4. Bước 3 — Bảng kết luận thẩm định rủi ro (lab04.md)

*Bảng đối chiếu kết luận thẩm định 3 hợp đồng, bắt buộc kèm chính xác số dòng mã làm bằng chứng theo quy định của Sổ tay thực hành ECO2432:*

| Hợp đồng | Kết luận | Tên hàm | Số dòng | Rủi ro cho người nắm giữ |
| :--- | :--- | :--- | :--- | :--- |
| **Hợp đồng A**<br>(`ClubTokenA`) | **An toàn / Không có quyền đặc biệt** | *Không có hàm đặc biệt* (`constructor` khởi tạo duy nhất) | Dòng 7–11 | **Không có rủi ro về mặt đặc quyền can thiệp hay lạm phát.**<br>- Hợp đồng không kế thừa `Ownable`, không có địa chỉ admin/owner sau khi triển khai.<br>- Tổng cung được đúc cố định 1,000,000 token ở dòng 9 và không có cơ chế nào để đúc thêm (*mint*) hay đóng băng ví người dùng. |
| **Hợp đồng B**<br>(`ClubTokenB`) | **Rủi ro cao**<br>*(Pha loãng vô hạn / Lạm phát mất giá)* | `mint(address to, uint256 amount)` | Dòng 18–20 | **Rủi ro pha loãng tài sản và xả hàng (Infinite Mint / Dump):**<br>- Quyền `onlyOwner` cho phép chủ sở hữu tự do đúc thêm số lượng token không giới hạn vào bất kỳ ví nào.<br>- Hợp đồng không thiết lập trần tổng cung (*cap*), không có cơ chế khóa thời gian (*timelock*) hay đa chữ ký (*multisig*).<br>- Chủ dự án có thể đúc hàng triệu token về ví riêng rồi bán tháo ra các bể thanh khoản (DEX), làm sập giá trị token mà nhà đầu tư đang nắm giữ về gần 0. |
| **Hợp đồng C**<br>(`ClubTokenC`) | **Rủi ro rất cao**<br>*(Bẫy lừa đảo Honeypot / Đóng băng tài sản)* | 1. `setRestricted(address user, bool status)`<br>2. `_update(address from, address to, uint256 value)` | 1. Dòng 30–32<br>2. Dòng 34–37 (điều kiện chặn tại **Dòng 35**) | **Rủi ro bị tước quyền sở hữu, khóa tài sản vĩnh viễn (Honeypot / Blacklist):**<br>- Chủ sở hữu hợp đồng (`onlyOwner`) có toàn quyền đưa bất kỳ địa chỉ ví nào vào danh sách hạn chế thông qua `restricted[user] = true` (dòng 31).<br>- Khi một ví bị đánh dấu `restricted`, dòng 35 `require(!restricted[from], "Dia chi bi han che");` sẽ chặn đứng mọi lệnh chuyển token đi từ ví đó.<br>- **Đặc trưng Honeypot:** Hợp đồng chỉ chặn chiều gửi (`from`), không chặn chiều nhận (`to`). Người dùng vẫn có thể nạp tiền hoặc mua token vào ví bình thường, nhưng khi muốn bán hoặc chuyển đi thì bị lỗi revert, dẫn đến mất trắng toàn bộ vốn đầu tư. |

---

## 5. Phân tích chuyên sâu & Bài học nghiệp vụ cho Chuyên viên Kinh tế số

### 5.1. Nhận diện các mẫu hình rủi ro thường gặp trong tài sản số
1. **Mẫu hình "Cửa sau đúc tiền" (Hidden Mint Backdoor - như Hợp đồng B):**
   - Dự án quảng cáo tổng cung giới hạn, nhưng mã nguồn lại âm thầm để ngỏ hàm `mint` có modifier quản trị.
   - Chuyên viên thẩm định cần kiểm tra: Nếu có hàm `mint`, phải có trần tối đa `maxSupply`, hoặc quyền `onlyOwner` phải được chuyển giao sang địa chỉ hủy (`address(0)`) hoặc hợp đồng quản trị DAO.
2. **Mẫu hình "Bẫy gián / Cấm bán" (Honeypot Mechanism - như Hợp đồng C):**
   - Đội ngũ lừa đảo thường dùng cơ chế này để giữ giá ảo của token tăng vọt trên các sàn DEX (vì chỉ có người mua vào, không ai bán ra được).
   - Trong phân tích tuân thủ: Cơ chế này tương tự như `blacklist` của USDT/USDC (đã học ở Lab 3), nhưng ở các dự án ẩn danh không có pháp nhân ràng buộc, 100% mục đích của nó là lừa đảo chiếm đoạt tài sản.

### 5.2. Giá trị của việc trích dẫn số dòng mã bằng chứng
- Trong báo cáo thẩm định đầu tư hoặc hồ sơ tuân thủ pháp lý, kết luận không thể dựa vào nhận định chung chung. Bắt buộc phải có **bằng chứng số dòng cụ thể** (ví dụ: dòng 18–20 cho hàm mint vô hạn, dòng 35 cho điều kiện chặn rút tiền). Đây là kỹ năng nền tảng của chuyên viên phân tích rủi ro on-chain (On-chain Risk Analyst).

---

## 6. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao thuc hanh lab 4 - nhan dien hop dong co rui ro"
git push
```
