# BÁO CÁO GIÁM ĐỊNH ON-CHAIN — FORENSICS.MD (LAB 3)

**Môn học:** TDT&HDTM / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 3 — Đọc Giao Dịch và Hợp Đồng trên Etherscan  
**Thời lượng:** 75 phút · **Hình thức:** Cá nhân  
**Sản phẩm nộp:** `forensics.md`  

---

## 1. Thông tin chung
- **Họ và tên:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân (Ví sinh viên):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Địa chỉ ví bạn cùng thực hành (Ví bạn ghép cặp từ Lab 2):** `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`
- **Mã băm giao dịch phân tích (Tx Hash từ Lab 2):** [`0x33ef63895383c7c0a08b782225b620abef103cc426045e5aff7c63976e077aad`](https://sepolia.etherscan.io/tx/0x33ef63895383c7c0a08b782225b620abef103cc426045e5aff7c63976e077aad)
- **Mạng thử nghiệm (Network):** Ethereum Sepolia Testnet

---

## 2. Bước 1 — Mổ xẻ giao dịch của chính mình (Bảng 10 trường Etherscan)

Dán mã băm giao dịch từ Lab 2 ([`0x33ef63895383c7c0a08b782225b620abef103cc426045e5aff7c63976e077aad`](https://sepolia.etherscan.io/tx/0x33ef63895383c7c0a08b782225b620abef103cc426045e5aff7c63976e077aad)) vào `https://sepolia.etherscan.io`. Bảng giải thích chi tiết 10 trường dữ liệu chuẩn nghiệp vụ:

| STT | Trường dữ liệu | Giá trị thực tế trên Sepolia Etherscan | Ý nghĩa kỹ thuật | Vì sao người làm nghiệp vụ cần (Góc độ Kế toán & Tuân thủ AML) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Status** | `Success` (Thành công) | Cho biết giao dịch đã được máy ảo EVM thực thi hoàn tất và ghi vào sổ cái hay bị đảo ngược (*reverted*). | Giao dịch thất bại **vẫn mất phí gas** — ảnh hưởng trực tiếp đến việc hạch toán chi phí và đối soát trạng thái giao dịch nạp/rút tiền của khách hàng. |
| 2 | **Block** | `10089738` (> 1,700,000 Block Confirmations) | Số thứ tự của khối chứa giao dịch trên blockchain Sepolia. | Xác định chính xác thời điểm ghi nhận vào sổ cái; đếm số lượt xác nhận (*block confirmations*) nhằm phòng ngừa rủi ro chuỗi bị phân nhánh (*reorganization*). |
| 3 | **Timestamp** | `Jan-21-2026 05:30:36 AM +UTC` (Unix: `1768973436`) | Mốc thời gian validator đóng gói khối chứa giao dịch lên mạng lưới. | Mốc xác định doanh thu / chi phí theo kỳ kế toán, xác định kỳ tính thuế và áp tỷ giá hối đoái giao dịch tài sản số tại thời điểm phát sinh. |
| 4 | **From / To** | **From:** `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`<br>**To:** `0x82d022a704706B2f144863D619D7418F8a0f19A7` | Địa chỉ ví gửi (bên ký ủy quyền giao dịch) và địa chỉ ví nhận (bên thụ hưởng). | Đối tượng cần xác minh danh tính (KYC/AML), rà soát danh sách đen/cấm vận quốc tế và xác định quyền sở hữu tài sản pháp lý. |
| 5 | **Value** | `3 ETH` (Sepolia ETH) | Lượng tài sản gốc (ETH) được chuyển giao giữa hai địa chỉ ví. | Giá trị hợp đồng/giao dịch kinh tế cần ghi nhận tăng/giảm trên bảng cân đối kế toán tài sản số. |
| 6 | **Transaction Fee** | `0.000054260244192 ETH` | Tổng chi phí gas thực tế thanh toán cho mạng lưới để xử lý giao dịch. | Chi phí hạ tầng vận hành mạng, cần hạch toán tách biệt vào tài khoản chi phí tài chính / chi phí hoạt động doanh nghiệp (không được tính gộp vào tiền chuyển). |
| 7 | **Gas Price** | `2.583821152 Gwei`<br>*(Base Fee: 1.084 Gwei \| Priority Fee: 1.5 Gwei)* | Đơn giá cho mỗi đơn vị gas tại thời điểm xử lý giao dịch (theo cơ chế EIP-1559). | Giải thích vì sao cùng một loại giao dịch nhưng thực hiện ở các thời điểm nghẽn mạng khác nhau lại tốn chi phí khác nhau; hỗ trợ tối ưu thời điểm gửi lệnh. |
| 8 | **Gas Limit** | `31,500` | Lượng gas tối đa mà ví người gửi cho phép máy ảo EVM tiêu thụ cho giao dịch. | Đặt quá thấp $\rightarrow$ giao dịch thất bại vì hết gas (*Out of Gas*) nhưng **vẫn mất phí**. Đặt quá cao $\rightarrow$ ví cần tạm khóa nhiều số dư hơn để bảo đảm thanh toán. |
| 9 | **Gas Used** | `21,000` (Tỷ lệ tiêu thụ: `66.67%` của Gas Limit) | Lượng tài nguyên tính toán thực tế mà mạng lưới đã tiêu thụ để hoàn tất giao dịch chuyển ETH tiêu chuẩn. | Cùng Gas Price với Gas Used tính ra phí thực trả:<br>$$\text{Transaction Fee} = \text{Gas Used} \times \text{Gas Price}$$<br>$21,000 \times 2.583821152 \times 10^{-9} = 0.000054260244192\text{ ETH}$.<br>$\text{Gas Used} = \text{Gas Limit}$ là dấu hiệu cảnh báo lỗi hết gas (*Out of Gas*). |
| 10 | **Nonce** | `87` (Vị trí trong khối: `13`) | Số thứ tự giao dịch phát xuất từ địa chỉ ví gửi `0x2e4216e...`. | Phát hiện giao dịch bị bỏ sót, bị kẹt trong hàng đợi mempool hoặc đã bị thay thế (*Speed Up / Cancel*); bảo vệ chống tấn công phát lại (*replay attack*). |

> **Đối chiếu giao dịch bổ sung:**
> - Chiều giao dịch chuyển testnet từ ví sinh viên (`0x82d022...`): [`0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d`](https://sepolia.etherscan.io/tx/0xf1b9c7586f805b0bcb6573d7e21518b6305a1103d457ccfb166e2f3170c1131d) (Block `11673318`, Phí: `0.00005222 ETH`).
> - Giao dịch đối ứng mẫu nội bộ: [`0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3`](https://sepolia.etherscan.io/tx/0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3) (Block `10109994`, Phí: `0.00005393 ETH`).

---

## 3. Bước 2 — Đọc một hợp đồng thật trên Ethereum Mainnet

Mở và phân tích hợp đồng **USDT** và **USDC** trên mạng chính Ethereum tại `https://etherscan.io`:

### 3.1. Phân biệt hợp đồng nguyên khối và hợp đồng Proxy (Chuẩn EIP-1967)
- **Tether USD (USDT)** — Địa chỉ: [`0xdAC17F958D2ee523a2206206994597C13D831ec7`](https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7):
  + Kiến trúc hợp đồng nguyên khối trực tiếp (`TetherToken`).
  + Các hàm nghiệp vụ hiển thị trực tiếp trong các tab **Read Contract** và **Write Contract**.
- **USD Coin (USDC)** — Địa chỉ: [`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`](https://etherscan.io/address/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48):
  + Kiến trúc hợp đồng ủy quyền có thể nâng cấp (*Upgradeable Proxy*) theo chuẩn **EIP-1967**.
  + Tab **Read/Write Contract** tại địa chỉ proxy chỉ hiển thị các hàm quản trị proxy kỹ thuật (`upgradeTo`, `changeAdmin`, `implementation`).
  + Muốn đọc hoặc gọi các hàm token nghiệp vụ (`totalSupply`, `balanceOf`, `blacklist`, `mint`...), kiểm toán viên phải chọn tab con **Read as Proxy** và **Write as Proxy**.
  + **Bài học nghiệp vụ cốt lõi:** Mã nguồn đã xác thực của hợp đồng Proxy chỉ là vỏ bọc điều hướng lệnh (`delegatecall`), logic kinh tế thực sự nằm tại địa chỉ **Implementation** mà proxy trỏ tới.

### 3.2. Ba thành phần quan trọng trong tab Contract trên Etherscan
1. **Bytecode (Mã máy):** Chuỗi ký tự thập lục phân nhị phân (`0x6080604052...`) được máy ảo EVM thực thi trực tiếp. Con người không thể đọc hiểu nghiệp vụ từ bytecode.
2. **Source Code (Verified - Mã nguồn đã xác thực):** Mã nguồn viết bằng ngôn ngữ bậc cao (Solidity/Vyper) do bên phát hành công bố công khai, được Etherscan biên dịch lại độc lập và đối chiếu khớp chính xác 100% với Bytecode trên chuỗi.
   > **Cảnh báo tuân thủ:** Nếu một dự án không công bố mã nguồn đã xác thực, đó là dấu hiệu cảnh báo rủi ro cao (*Red Flag*), tiềm ẩn nguy cơ cửa sau (*backdoor*), mã độc hoặc lừa đảo rút cạn thanh khoản (*rug pull*).
3. **Phân biệt Read Contract vs. Write Contract:**
   - **Tab Read Contract (Hàm đọc):** Các hàm chỉ truy vấn dữ liệu từ blockchain (từ khóa `view` hoặc `pure`). Không làm thay đổi trạng thái sổ cái $\rightarrow$ **Hoàn toàn miễn phí, không tốn gas, không cần kết nối ví Web3.** (Ví dụ: gọi `totalSupply()`, `balanceOf()`).
   - **Tab Write Contract (Hàm ghi):** Các hàm làm thay đổi dữ liệu trên sổ cái blockchain $\rightarrow$ **Bắt buộc phải kết nối ví, ký xác nhận giao dịch và thanh toán phí gas.** (Ví dụ: `transfer()`, `blacklist()`).

---

## 4. Bước 3 — Ghi nhận & Trả lời 3 câu hỏi bắt buộc

### Câu 1: Hợp đồng bạn xem có công bố mã nguồn đã xác thực không?
**Trả lời:** **CÓ**.
- **Đối với Tether USD (USDT - `0xdAC17F958D2ee523a2206206994597C13D831ec7`):**
  + Hợp đồng `TetherToken` có dấu tích xanh xác nhận **Contract Source Code Verified (Exact Match)** trên Etherscan.
  + Trình biên dịch: Solidity phiên bản `v0.4.18+commit.9cf6e910`, tối ưu hóa 200 runs. Mã nguồn công khai hoàn toàn minh bạch.
- **Đối với USD Coin (USDC - `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`):**
  + Cả hợp đồng `FiatTokenProxy` (EIP-1967) và hợp đồng logic triển khai `FiatTokenV2_2` đều đạt trạng thái **Verified** trên Etherscan.

---

### Câu 2: Tổng cung của đồng đó là bao nhiêu? Đọc ra từ hàm nào?
**Trả lời:**
- **Hàm đọc dữ liệu:** Hàm **`totalSupply()`** trong tab **Read Contract** (với USDT) hoặc tab **Read as Proxy** (với USDC).
- **Số liệu ghi nhận thực tế trên Ethereum Mainnet:**
  + **Tether USD (USDT):**
    * Giá trị nguyên thô (raw value) trả về từ hàm `totalSupply()`: `88,304,342,264,551,152` đơn vị.
    * Do USDT sử dụng `decimals = 6` (1 USDT = $10^6$ đơn vị nhỏ nhất), tổng cung thực tế là:
      $$\text{Total Supply}_{\text{USDT}} = \frac{88,304,342,264,551,152}{10^6} \approx \mathbf{88,304,342,264.55\text{ USDT}}$$
      *(Xấp xỉ hơn 88.3 tỷ USDT lưu hành trên mạng Ethereum).*
  + **USD Coin (USDC):**
    * Giá trị nguyên thô trả về từ hàm `totalSupply()` trong tab *Read as Proxy*: `50,416,450,055,766,768` đơn vị.
    * Với `decimals = 6`, tổng cung thực tế là:
      $$\text{Total Supply}_{\text{USDC}} = \frac{50,416,450,055,766,768}{10^6} \approx \mathbf{50,416,450,055.77\text{ USDC}}$$
      *(Xấp xỉ hơn 50.4 tỷ USDC lưu hành trên mạng Ethereum).*

---

### Câu 3 (Quan trọng nhất): Trong tab Write Contract (với USDC: Write as Proxy), có hàm nào cho phép một địa chỉ đặc biệt đóng băng tài khoản người khác không? Nếu có, tên hàm là gì?

**Trả lời:** **CÓ, cả hai đồng ổn định giá lớn nhất thế giới đều tích hợp cơ chế đóng băng tài khoản người khác.**

#### Chi tiết tên hàm và phân quyền kiểm soát:
1. **Đối với USDC (xem trong tab *Write as Proxy*):**
   - **Tên hàm đóng băng:** **`blacklist(address _account)`**
   - **Tên hàm gỡ bỏ đóng băng:** **`unBlacklist(address _account)`**
   - **Hàm kiểm tra trạng thái (tab Read as Proxy):** **`isBlacklisted(address _account)`**
   - **Phân quyền thực thi:** Hàm được bảo vệ bởi modifier `onlyBlacklister`. Chỉ duy nhất địa chỉ ví được tổ chức phát hành (Centre Consortium / Circle) cấp quyền `blacklister` mới có quyền thực thi. Khi tài khoản bị đưa vào danh sách đen, mọi giao dịch nạp và rút (`transfer`, `transferFrom`) liên quan đến tài khoản đó đều bị revert ngay lập tức.
2. **Đối với USDT (xem trong tab *Write Contract*):**
   - **Tên hàm đóng băng:** **`addBlackList(address _evilUser)`**
   - **Tên hàm gỡ bỏ đóng băng:** **`removeBlackList(address _clearedUser)`**
   - **Hàm tiêu hủy tài sản của ví bị khóa:** **`destroyBlackFunds(address _blackListedUser)`**
   - **Phân quyền thực thi:** Hàm được bảo vệ bởi modifier `onlyOwner`. Chỉ duy nhất địa chỉ Owner quản trị của Tether Limited mới có quyền gọi. Khi một ví bị gán `isBlackListed[_evilUser] = true`, toàn bộ số dư USDT trong ví đó bị đóng băng hoàn toàn và Tether có quyền hủy bỏ vĩnh viễn số tiền đó khỏi lưu thông.

#### Thảo luận mở rộng về mức độ phi tập trung thực tế:
- **Vỡ mộng về tính "phi tập trung tuyệt đối":** Phần lớn sinh viên và người mới tham gia Web3 thường lầm tưởng rằng mọi tài sản mã hóa đều có tính chất phi tập trung tuyệt đối và không ai có thể can thiệp vào ví cá nhân. Tuy nhiên, thực tế là các đồng tiền ổn định giá hàng đầu (USDT, USDC) — vốn là huyết mạch thanh khoản của nền kinh tế Web3 — đều có quyền kiểm soát tập trung tuyệt đối (*Centralized Control*).
- **Lý do tồn tại cơ chế đóng băng (Góc độ Tuân thủ & Pháp lý):**
  + Các tổ chức phát hành (Circle, Tether) phải chịu sự giám sát pháp lý chặt chẽ từ Bộ Tài chính Hoa Kỳ, Văn phòng Kiểm soát Tài sản Nước ngoài (OFAC) và các quy chuẩn quốc tế về phòng chống rửa tiền (AML/CFT).
  + Khi nhận được trát tòa hoặc yêu cầu từ các cơ quan hành pháp quốc tế về việc phong tỏa ví của tin tặc (hacker), dòng tiền lừa đảo hoặc đối tượng nằm trong danh sách trừng phạt kinh tế, tổ chức phát hành bắt buộc phải kích hoạt hàm `blacklist` / `addBlackList`.
- **Kết luận cho sinh viên Kinh tế số:** Khi phân tích on-chain và thẩm định rủi ro tài sản số, không bao giờ được đánh giá một token chỉ qua các lời hứa phi tập trung. Chuyên viên nghiệp vụ phải trực tiếp mở tab **Contract** trên Etherscan, rà soát các đặc quyền can thiệp (`onlyOwner`, `onlyBlacklister`, `pause`, `upgradeTo`) để xác định chính xác mức độ tập trung quyền lực và rủi ro kiểm duyệt (*censorship risk*) của tài sản.

---

## 5. Giá trị bài học đối với công việc thực tế
- **Chuyên viên Tuân thủ (AML / KYC Officer):** Nắm vững 10 trường giao dịch giúp truy vết nhanh nguồn gốc tài sản, phát hiện dấu hiệu rửa tiền, liên kết dòng tiền giữa các ví vệ tinh.
- **Kế toán tài sản số (Crypto Accounting):** Xác định chính xác giá trị thực chuyển, thời điểm ghi nhận theo timestamp khối và bóc tách riêng chi phí giao dịch (Transaction Fee = Gas Used × Gas Price) phục vụ quyết toán thuế và lập báo cáo tài chính chuẩn mực.
- **Thẩm định rủi ro on-chain (On-chain Risk Analyst):** Phân biệt mã máy với mã nguồn đã xác thực, nhận diện kiến trúc Proxy EIP-1967 và kiểm tra các hàm đặc quyền kiểm soát tài sản trước khi tư vấn đầu tư hoặc tích hợp thanh toán.

---

## 6. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs(lab-03): hoan thanh bao cao giam dinh on-chain tren etherscan (forensics.md)"
git push
```
