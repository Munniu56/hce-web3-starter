# BÁO CÁO GIÁM ĐỊNH ON-CHAIN — FORENSICS.MD (LAB 3)

**Môn học:** Kinh tế số / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 3 — Đọc Giao Dịch và Hợp Đồng trên Etherscan  
**Thời lượng:** 75 phút · **Hình thức:** Cá nhân  
**Sản phẩm nộp:** `forensics.md`  

---

## 1. Thông tin chung
- **Họ và tên:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh te so
- **Địa chỉ ví cá nhân (Ví gửi - Sinh viên):** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`
- **Địa chỉ ví bạn cùng thực hành (Ví nhận):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Mã băm giao dịch phân tích (Tx Hash từ Lab 2):** [`0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3`](https://sepolia.etherscan.io/tx/0x199e95f10417bb93a1b81ddad2450e0ac4104af985f7a09910eb7506a1cf98a3)
- **Mạng thử nghiệm (Network):** Ethereum Sepolia Testnet

---

## 2. Bước 1 — Mổ xẻ giao dịch của chính mình (Bảng 10 trường Etherscan)

| STT | Trường dữ liệu | Giá trị thực tế trên Sepolia Etherscan | Ý nghĩa kỹ thuật | Vì sao người làm nghiệp vụ cần (Góc độ Kế toán & Tuân thủ AML) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Status** | `Success` (Thành công) | Cho biết giao dịch đã được EVM thực thi hoàn tất hay bị đảo ngược (*reverted*). | Giao dịch thất bại **vẫn mất phí** — ảnh hưởng trực tiếp đến hạch toán chi phí và đối soát trạng thái giao dịch khách hàng. |
| 2 | **Block** | `10109994` (1,665,850+ Block Confirmations) | Số thứ tự khối chứa giao dịch trên chuỗi khối Sepolia. | Xác định thời điểm ghi nhận sổ cái và tính số lượt xác nhận (block confirmations) nhằm phòng ngừa rủi ro chuỗi bị phân nhánh (*reorganization*). |
| 3 | **Timestamp** | `Jan-24-2026 01:57:36 AM +UTC` (Unix: `1769219856`) | Mốc thời gian validator đóng gói và ghi nhận khối chứa giao dịch. | Mốc xác định doanh thu / chi phí theo kỳ kế toán, xác định kỳ tính thuế và áp tỷ giá hối đoái tại thời điểm phát sinh giao dịch. |
| 4 | **From / To** | **From:** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`<br>**To:** `0x82d022a704706B2f144863D619D7418F8a0f19A7` | Địa chỉ ví gửi (bên ký giao dịch) và địa chỉ ví nhận (bên thụ hưởng). | Đối tượng cần xác minh danh tính (KYC/AML), rà soát danh sách đen/cấm vận quốc tế và xác định quyền sở hữu tài sản. |
| 5 | **Value** | `4 ETH` | Lượng tài sản gốc (ETH) được chuyển dịch giữa hai tài khoản. | Giá trị hợp đồng/giao dịch kinh tế cần ghi nhận tăng/giảm trên bảng cân đối kế toán tài sản số. |
| 6 | **Transaction Fee** | `0.000053933790708 ETH` | Tổng chi phí gas thực trả cho mạng lưới để xử lý giao dịch. | Chi phí hạ tầng vận hành mạng, cần hạch toán tách biệt vào tài khoản chi phí tài chính / chi phí hoạt động doanh nghiệp. |
| 7 | **Gas Price** | `2.568275748 Gwei`<br>*(Base: 1.068 Gwei \| Max: 2.915 Gwei \| Priority: 1.5 Gwei)* | Đơn giá gas tại thời điểm xử lý giao dịch (theo cơ chế EIP-1559). | Giải thích vì sao cùng một loại giao dịch nhưng thực hiện ở các thời điểm khác nhau lại tốn chi phí khác nhau; hỗ trợ tối ưu thời điểm gửi lệnh. |
| 8 | **Gas Limit** | `31,500` | Mức gas tối đa ví người gửi cho phép EVM tiêu thụ cho giao dịch này. | Đặt quá thấp $\rightarrow$ giao dịch thất bại vì hết gas (*Out of Gas*) nhưng **vẫn mất phí**. Đây là trần kiểm soát rủi ro chi phí của bên gửi. |
| 9 | **Gas Used** | `21,000` (Tỷ lệ tiêu thụ: `66.67%` của Gas Limit) | Lượng tài nguyên tính toán thực tế mà mạng lưới đã tiêu thụ. | Cùng Gas Price với Gas Used tính ra phí:<br>$$\text{Fee} = \text{Gas Used} \times \text{Gas Price}$$<br>$21,000 \times 2.568275748 \times 10^{-9} = 0.000053933790708\text{ ETH}$.<br>$\text{Gas Used} = \text{Gas Limit}$ là dấu hiệu cảnh báo lỗi hết gas. |
| 10 | **Nonce** | `52` (Vị trí trong khối: `5`) | Số thứ tự giao dịch phát xuất từ địa chỉ ví gửi `0x5856B2C...`. | Phát hiện giao dịch bị bỏ sót, bị kẹt trong hàng đợi mempool hoặc đã bị thay thế (*Speed Up / Cancel*); bảo vệ chống tấn công phát lại (*replay attack*). |

---

## 3. Bước 2 — Đọc hợp đồng thực tế (USDT & USDC trên Ethereum Mainnet)

### 3.1. Phân biệt hợp đồng nguyên khối và hợp đồng Proxy (EIP-1967)
- **Tether USD (USDT)** — Địa chỉ: [`0xdAC17F958D2ee523a2206206994597C13D831ec7`](https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7):
  + Kiến trúc hợp đồng nguyên khối trực tiếp (`TetherToken`).
  + Các hàm nghiệp vụ hiển thị trực tiếp trong các tab **Read Contract** và **Write Contract**.
- **USD Coin (USDC)** — Địa chỉ: [`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`](https://etherscan.io/address/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48):
  + Kiến trúc hợp đồng có thể nâng cấp (*Upgradeable Proxy*) theo chuẩn **EIP-1967**.
  + Tab **Read/Write Contract** tại địa chỉ proxy chỉ hiển thị các hàm quản trị proxy kỹ thuật (`upgradeTo`, `changeAdmin`, `implementation`).
  + Muốn đọc hoặc gọi các hàm token nghiệp vụ (`totalSupply`, `balanceOf`, `blacklist`, `mint`...), kiểm toán viên phải chọn tab con **Read as Proxy** và **Write as Proxy**.
  + **Bài học nghiệp vụ cốt lõi:** Mã nguồn đã xác thực của hợp đồng Proxy chỉ là vỏ bọc điều hướng lệnh (`delegatecall`), logic kinh tế thực sự nằm tại địa chỉ **Implementation** mà proxy trỏ tới.

### 3.2. Ba thành phần quan trọng trong tab Contract trên Etherscan
1. **Bytecode (Mã máy):** Chuỗi ký tự thập lục phân (`0x6080604052...`) được máy ảo EVM thực thi. Con người không thể đọc hiểu trực tiếp.
2. **Source Code (Verified - Mã nguồn đã xác thực):** Mã nguồn viết bằng ngôn ngữ bậc cao (Solidity/Vyper) do nhà phát hành công bố công khai, được Etherscan biên dịch lại độc lập và đối chiếu khớp chính xác 100% với Bytecode trên chuỗi.
   > **Cảnh báo tuân thủ:** Nếu một dự án không công bố mã nguồn đã xác thực, hợp đồng đó là một "hộp đen" hoàn toàn, tiềm ẩn nguy cơ cao về mã độc, cửa sau (*backdoor*), hoặc lừa đảo rút cạn tiền (*rug pull*).
3. **Phân biệt Read Contract vs. Write Contract:**
   - **Tab Read Contract (Hàm đọc):** Chỉ đọc dữ liệu từ blockchain (từ khóa `view` hoặc `pure`). Không làm thay đổi trạng thái sổ cái $\rightarrow$ **Hoàn toàn miễn phí, không tốn phí gas, không yêu cầu ví kết nối.**
   - **Tab Write Contract (Hàm ghi):** Làm thay đổi trạng thái dữ liệu trên sổ cái $\rightarrow$ **Bắt buộc phải kết nối ví Web3, ký xác nhận giao dịch và trả phí gas.**

---

## 4. Bước 3 — Trả lời 3 câu hỏi bắt buộc (Trọng tâm bài Lab)

### Câu 1: Hợp đồng bạn xem có công bố mã nguồn đã xác thực không?
**Trả lời:** **CÓ**.
- **Đối với Tether USD (USDT - `0xdAC17F958D2ee523a2206206994597C13D831ec7`):**
  + Hợp đồng `TetherToken` có dấu tích xanh xác nhận **Contract Source Code Verified (Exact Match)** trên Etherscan.
  + Trình biên dịch: Solidity phiên bản `v0.4.18+commit.9cf6e910`, tối ưu hóa bật 200 runs. Mã nguồn công khai hoàn toàn minh bạch.
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
   - **Phân quyền thực thi:** Hàm được bảo vệ bởi modifier `onlyBlacklister`. Chỉ duy nhất địa chỉ ví được tổ chức phát hành (Centre Consortium / Circle) cấp quyền `blacklister` mới có quyền thực thi. Khi tài khoản bị đưa vào danh sách đen, mọi giao dịch chuyển tiền (`transfer`, `transferFrom`) liên quan đến tài khoản đó đều bị revert.
2. **Đối với USDT (xem trong tab *Write Contract*):**
   - **Tên hàm đóng băng:** **`addBlackList(address _evilUser)`**
   - **Tên hàm gỡ bỏ đóng băng:** **`removeBlackList(address _clearedUser)`**
   - **Hàm tiêu hủy tài sản của ví bị khóa:** **`destroyBlackFunds(address _blackListedUser)`**
   - **Phân quyền thực thi:** Hàm được bảo vệ bởi modifier `onlyOwner`. Chỉ duy nhất địa chỉ Owner quản trị của Tether Limited mới có quyền gọi. Khi một ví bị gán `isBlackListed[_evilUser] = true`, toàn bộ số dư USDT trong ví đó bị đóng băng hoàn toàn và Tether thậm chí có quyền đốt bỏ vĩnh viễn số tiền đó.

#### Thảo luận mở rộng về mức độ phi tập trung thực tế:
- **Vỡ mộng về tính "phi tập trung tuyệt đối":** Phần lớn người mới tham gia Web3 lầm tưởng rằng tiền mã hóa là phi tập trung 100% và không ai có thể can thiệp vào tài sản trong ví của mình. Tuy nhiên, các đồng tiền ổn định giá (Stablecoins) tập trung như USDT hay USDC đóng vai trò là mạch máu thanh khoản của toàn bộ thị trường tiền mã hóa lại chứa đựng quyền kiểm soát tập trung tuyệt đối (*Centralized Control*).
- **Lý do tồn tại cơ chế đóng băng (Góc độ Tuân thủ & Pháp lý):**
  + Các tổ chức phát hành như Circle hay Tether chịu sự giám sát pháp lý chặt chẽ từ Bộ Tài chính Hoa Kỳ, cơ quan kiểm soát tài sản ngoại quốc (OFAC) và các hiệp ước phòng chống rửa tiền quốc tế (AML/CFT).
  + Khi phát hiện các địa chỉ ví liên quan đến tấn công hacker sàn giao dịch, lừa đảo xuyên biên giới, tài trợ khủng bố hoặc nằm trong danh sách cấm vận kinh tế, tổ chức phát hành bắt buộc phải kích hoạt hàm `blacklist` / `addBlackList` theo trát của tòa án hoặc lệnh điều tra.
- **Kết luận cho sinh viên Kinh tế số:** Khi phân tích on-chain và thẩm định rủi ro dự án, không bao giờ được đánh giá một token chỉ dựa trên lời quảng bá. Chuyên viên nghiệp vụ phải trực tiếp mở tab **Contract** trên Etherscan, tra cứu các hàm phân quyền quản trị (`onlyOwner`, `onlyAdmin`, `onlyBlacklister`, `pause`, `mint`) để định lượng chính xác mức độ tập trung và rủi ro kiểm duyệt (*censorship risk*) của tài sản đó.

---

## 5. Giá trị bài học đối với công việc thực tế
- **Chuyên viên Tuân thủ (AML / KYC Officer):** Kỹ năng mổ xẻ 10 trường giao dịch giúp nhanh chóng phát hiện các dấu hiệu bất thường (đột biến gas price nhằm ưu tiên giao dịch, chuỗi nonce liên tiếp, dòng tiền luân chuyển giữa các ví liên quan).
- **Kế toán tài sản số (Crypto Accounting):** Xác định chính xác giá trị thực chuyển, thời điểm ghi nhận theo timestamp khối và bóc tách riêng chi phí giao dịch (Transaction Fee = Gas Used × Gas Price) phục vụ quyết toán thuế và lập báo cáo tài chính.
- **Thẩm định rủi ro on-chain (On-chain Risk Analyst):** Phân biệt mã máy với mã nguồn đã xác thực và kiểm tra kỹ lưỡng các hàm can thiệp quyền sở hữu (đóng băng, tạm dừng, nâng cấp proxy) trước khi tích hợp vào hệ thống tài chính của doanh nghiệp.

---

## 6. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao thuc hanh lab 3 - doc giao dich va hop dong tren etherscan (forensics.md)"
git push
```
