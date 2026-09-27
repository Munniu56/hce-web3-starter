# BÁO CÁO THỰC HÀNH — LAB 7: TÍNH CHI PHÍ VẬN HÀNH THỰC TẾ

**Môn học:** Kinh tế số / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 7 — Tính chi phí vận hành thực tế  
**Thời lượng:** 75 phút · **Hình thức:** Nhóm 2 người  
**Sản phẩm nộp quy định:** `lab07.md` gồm bảng tính và kết luận về tính khả thi  

---

## 1. Thông tin chung
- **Họ và tên sinh viên thực hiện:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh tế số
- **Địa chỉ ví cá nhân:** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`
- **Tệp báo cáo:** [`Lab 1-7/lab07.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/lab07.md)

---

## 2. Ý nghĩa kinh tế của bài Lab (Gắn với công việc thực tế)
> *"Đây là bài toán kinh tế, không phải bài toán kỹ thuật — và là phần sinh viên Kinh tế làm tốt hơn sinh viên CNTT. Một sản phẩm chạy được nhưng chi phí giao dịch cao hơn giá trị giao dịch thì không có mô hình kinh doanh."*

Một hợp đồng thông minh dù được viết tối ưu và bảo mật đến đâu, nếu không giải quyết được bài toán chi phí vận hành (Unit Economics) thì không thể đưa vào đời sống. Vai trò của Chuyên viên Phân tích Nghiệp vụ (BA) và Chuyên viên Kinh tế số là:
1. Dự báo chính xác chi phí vận hành hạ tầng blockchain (Gas Overhead) trước khi triển khai.
2. Thiết kế mô hình phân bổ chi phí (Cost Allocation): Ai là người chịu phí? Phí có cản trở hành vi người dùng hay không?
3. Lựa chọn hạ tầng phù hợp: Nhận diện ranh giới giữa mạng Lớp 1 (Layer 1 - Ethereum Mainnet) và mạng Lớp 2 (Layer 2 - Arbitrum, Optimism, Base).

---

## 3. Bước 1 — Cấu trúc phí giao dịch trên mạng Ethereum

Công thức nền tảng tính chi phí một giao dịch trên blockchain:
$$\text{Chi phí giao dịch (ETH)} = \text{Lượng gas tiêu thụ (Gas Used)} \times \text{Đơn giá gas (Gas Price in Gwei)} \times 10^{-9}$$
$$\text{Chi phí giao dịch (USD)} = \text{Chi phí giao dịch (ETH)} \times \text{Giá ETH tại thời điểm tính (USD)}$$

### Bảng tham khảo mức tiêu thụ Gas theo loại thao tác EVM

| STT | Loại thao tác | Lượng gas tham khảo | Bản chất kỹ thuật trên EVM |
| :-: | :--- | :---: | :--- |
| 1 | **Chuyển ETH thông thường** | `21.000` | Mức gas cơ sở tối thiểu cho mọi giao dịch thanh toán cơ bản giữa hai tài khoản EOA. |
| 2 | **Chuyển token ERC-20** | `~50.000 – 65.000` | Gọi hàm `transfer()`, đọc và ghi lại số dư của 2 tài khoản trong mapping lưu trữ. |
| 3 | **Ghi biến mới vào bộ nhớ dài hạn (`SSTORE`)** | `~20.000` | Thao tác ghi ô nhớ từ giá trị `0` sang giá trị khác `0` (chiếm dụng tài nguyên lưu trữ vĩnh viễn của node). |
| 4 | **Sửa một biến đã có trong bộ nhớ (`SSTORE`)** | `~5.000` | Thay đổi ô nhớ đã có sẵn dữ liệu khác `0` sang một giá trị mới (tốn ít tài nguyên hơn). |
| 5 | **Triển khai hợp đồng cỡ nhỏ (Deploy)** | `~500.000 – 1.500.000` | Lưu trữ toàn bộ bytecode của hợp đồng lên blockchain và thực thi hàm `constructor`. |

---

## 4. Bước 2 — Bài toán kinh tế: Thẻ tích điểm Câu lạc bộ Sinh viên

### Đề bài
Một câu lạc bộ sinh viên phát hành thẻ tích điểm trên blockchain. 
- Tần suất: **1.000 lượt cộng điểm/tháng**.
- Bản chất mỗi lượt: **Một giao dịch ghi dữ liệu vào hợp đồng thông minh** (lượng gas tham khảo: `20.000` gas cho thao tác ghi dữ liệu `SSTORE`, hoặc `~45.000` gas nếu tính toàn bộ hàm giao dịch tích điểm của smart contract).
- Giả định tham chiếu:
  + Đơn giá gas: 20 Gwei ($20 \times 10^{-9}\text{ ETH}$).
  + Giá ETH tham chiếu: 3.000 USD/ETH.
  + Tỷ giá quy đổi giả định: 1 USD = 25.400 VNĐ.

---

### a. Chi phí vận hành một tháng trên mạng Ethereum Layer 1 (USD & VNĐ)

Áp dụng công thức tính chi phí:
- **Lượng gas tiêu thụ:** $G = 20.000\text{ gas}$ (theo mốc chuẩn thao tác ghi dữ liệu).
- **Phí một lượt cộng điểm (ETH):**
  $$\text{Fee}_{\text{1 tx}} = 20.000 \times 20 \times 10^{-9} = 0,0004\text{ ETH}$$
- **Phí một lượt cộng điểm (USD):**
  $$\text{Fee}_{\text{1 tx (USD)}} = 0,0004\text{ ETH} \times 3.000\text{ USD} = 1,20\text{ USD} \quad (\approx 30.480\text{ VNĐ})$$
- **Tổng chi phí 1 tháng cho 1.000 lượt cộng điểm:**
  $$\text{Chi phí tháng}_{\text{L1}} = 1.000 \times 1,20\text{ USD} = \mathbf{1.200\text{ USD/tháng}} \quad (\mathbf{\approx 30.480.000\text{ VNĐ/tháng}})$$

*(Ghi chú mở rộng: Nếu tính theo hàm giao dịch token đầy đủ tiêu thụ 45.000 gas, chi phí mỗi giao dịch là 2,70 USD, tổng chi phí hàng tháng lên tới **2.700 USD/tháng**, tương đương **68.580.000 VNĐ/tháng**).*

---

### b. Chi phí khi chuyển sang mạng Layer 2 (Rẻ hơn khoảng 100 lần)

Mạng Layer 2 (như Arbitrum, Optimism, Base) sử dụng công nghệ gom giao dịch (*Rollup*) giúp giảm phí khoảng 100 lần so với Layer 1:
- **Tỷ lệ giảm phí:** Giảm $100$ lần (tương đương $1\%$).
- **Phí một lượt cộng điểm trên Layer 2:**
  $$\text{Fee}_{\text{1 tx (L2)}} = \frac{1,20\text{ USD}}{100} = \mathbf{0,012\text{ USD}} \quad (\approx 305\text{ VNĐ})$$
- **Tổng chi phí một tháng cho 1.000 lượt cộng điểm:**
  $$\text{Chi phí tháng}_{\text{L2}} = \frac{1.200\text{ USD}}{100} = \mathbf{12\text{ USD/tháng}} \quad (\mathbf{\approx 304.800\text{ VNĐ/tháng}})$$

*(Nếu tính với mức 45.000 gas, chi phí trên L2 là **27 USD/tháng**, tương đương **685.800 VNĐ/tháng**).*

---

### c. Phân tích đối tượng chịu phí: Câu lạc bộ hay Sinh viên?

#### Tình huống 1: Câu lạc bộ (CLB) chi trả toàn bộ phí
- **Trên Layer 1 (1.200 USD $\approx$ 30,5 triệu VNĐ/tháng):**
  + **Bất khả thi tuyệt đối:** Ngân sách cả năm của một CLB sinh viên thường chỉ dao động từ 5 - 15 triệu VNĐ. Một tháng chi phí gas trên L1 đã vượt gấp 2–6 lần ngân sách của cả năm. CLB sẽ cạn kiệt tài chính ngay trong tuần đầu tiên hoạt động.
- **Trên Layer 2 (12 USD $\approx$ 305.000 VNĐ/tháng):**
  + **Hoàn toàn khả thi:** Con số 300.000 VNĐ/tháng nằm gọn trong khả năng trích quỹ thành viên hoặc nguồn tài trợ sự kiện. CLB có thể ứng dụng cơ chế **Account Abstraction (ERC-4337 / Paymaster)** để tài trợ gas tự động cho sinh viên, giúp sinh viên có trải nghiệm như đang dùng ứng dụng Web2 thông thường.

#### Tình huống 2: Sinh viên (người nhận điểm) tự chi trả phí
- **Trên Layer 1 (Mỗi lần tích điểm tốn 1,20 USD $\approx$ 30.500 VNĐ):**
  + **Sinh viên chắc chắn từ chối 100%:** Một điểm thưởng của CLB có giá trị kinh tế ước tính chỉ tương đương một vé giữ xe (5.000 VNĐ) hoặc giảm giá cốc trà sữa (10.000 - 20.000 VNĐ). Việc bắt sinh viên bỏ ra 30.500 VNĐ tiền gas để nhận một ưu đãi trị giá 10.000 VNĐ là một quyết định phi lý trí về mặt tài chính. Không một sinh viên nào chấp nhận sử dụng.
- **Trên Layer 2 (Mỗi lần tích điểm tốn 0,012 USD $\approx$ 305 VNĐ):**
  + Con số 300 VNĐ là chấp nhận được về mặt số tiền, nhưng **vẫn tồn tại rào cản hành vi nghiêm trọng**: Sinh viên phải cài ví MetaMask, phải mua ETH trên mạng Layer 2, và phải ký xác nhận cho từng lần điểm danh. Do đó, phương án tối ưu nhất vẫn là **CLB tài trợ khoản phí này qua Paymaster** trên Layer 2.

---

### d. Bảng so sánh tổng hợp và Kết luận về tính khả thi kinh tế

| Chỉ số kinh tế | Mạng Layer 1 (Ethereum Mainnet) | Mạng Layer 2 (Arbitrum / Optimism / Base) | Chênh lệch / Tác động |
| :--- | :---: | :---: | :---: |
| **Đơn giá Gas** | 20 Gwei | $\approx 0,2\text{ Gwei}$ (kèm Data Blob EIP-4844) | Rẻ hơn 100 lần |
| **Chi phí 1 lượt tích điểm** | **1,20 USD** (30.480 đ) | **0,012 USD** (305 đ) | Tiết kiệm 99% chi phí |
| **Tổng chi phí / tháng (1.000 tx)** | **1.200 USD** (30.480.000 đ) | **12 USD** (304.800 đ) | Giảm từ mức phá sản xuống mức khả thi |
| **Thời gian xác nhận khối** | 12 – 15 giây (có thể nghẽn) | $\approx 1 – 2\text{ giây}$ | Nhanh hơn 10 lần |
| **Khả năng CLB tài trợ gas** | ❌ Không thể gánh nổi | ✅ Hoàn toàn trong tầm tay | Mô hình vận hành bền vững |
| **Sự chấp nhận của sinh viên** | ❌ Từ chối tuyệt đối | ✅ Hào hứng đón nhận | Xóa bỏ rào cản gia nhập |
| **KẾT LUẬN TÍNH KHẢ THI** | ⛔ **KHÔNG KHẢ THI** |  **HOÀN TOÀN KHẢ THI** | **Bắt buộc triển khai trên L2** |

---

## 5. Bước 3 — Mở rộng: Tính toán chi phí cho Đồ án nhóm ECO2432

### Đề tài đồ án nhóm lựa chọn: Ký quỹ mua bán đồ cũ Ký túc xá (`SimpleEscrow`)
- **Mục đích:** Bảo vệ quyền lợi cho sinh viên mua bán đồ cũ (máy tính, tủ lạnh mini, giáo trình) tại KTX mà không sợ bị lừa đảo giao tiền trước không nhận được hàng.
- **Quy mô dự kiến một tháng:** **200 đơn giao dịch thành công**.

### Phân rã chuỗi thao tác của một hợp đồng ký quỹ hoàn chỉnh:
Một chu trình ký quỹ gồm 3 giao dịch on-chain:
1. `createAndFund()` (Người mua tạo đơn và nạp tiền cọc): $\approx 65.000\text{ gas}$.
2. `confirmReceived()` (Người mua xác nhận đã nhận hàng, tiền giải ngân cho người bán): $\approx 35.000\text{ gas}$.
3. `refundAfterDeadline()` (Xử lý hoàn tiền nếu trễ hạn giao hàng - ước tính chiếm 10% số ca): $\approx 30.000\text{ gas}$.
$\rightarrow$ **Trung bình một đơn hàng hoàn chỉnh tiêu thụ:** $\approx 100.000\text{ gas}$.

### Bảng dự toán chi phí vận hành đồ án trên Layer 1 vs Layer 2:

| Khoản mục chi phí | Đơn vị tính | Kịch bản Layer 1 (Ethereum) | Kịch bản Layer 2 (Base / Arbitrum) |
| :--- | :---: | :---: | :---: |
| **Lượng gas trung bình / đơn** | Gas | 100.000 | 100.000 |
| **Đơn giá gas giả định** | Gwei | 20 Gwei | 0,2 Gwei |
| **Chi phí gas cho 1 đơn hàng** | USD | **6,00 USD** (152.400 VNĐ) | **0,06 USD** (1.524 VNĐ) |
| **Giá trị đơn hàng đồ cũ bình quân** | VNĐ | 200.000 VNĐ | 200.000 VNĐ |
| **Tỷ lệ phí gas trên giá trị hàng** | % | **76,2%** (Vô lý về mặt kinh tế) | **0,76%** (Rất cạnh tranh) |
| **Tổng chi phí gas 200 đơn / tháng** | USD / tháng | **1.200 USD** (30.480.000 đ) | **12 USD** (304.800 đ) |
| **Mô hình thu phí đề xuất** | % | Không thể áp dụng vì phí gas quá cao | Trích 1,5% giá trị đơn ($\approx 3.000\text{ đ}$) để bù gas và tạo lợi nhuận |
| **Đánh giá tính khả thi đồ án** | Kết luận | ⛔ **Thất bại hoàn toàn** |  **Có mô hình kinh doanh bền vững** |

---

## 6. Bài học nghiệp vụ cốt lõi (Kết luận sư phạm)

> **Kết luận cần rút ra:** Câu hỏi (d) dẫn tự nhiên đến khái niệm **mạng Layer 2** — nội dung cốt lõi của **Session 02 về Mạng Lớp 2 (Layer 2 Scaling Solutions)**.

1. **Layer 1 không dành cho giao dịch vi mô:** Ethereum Layer 1 đóng vai trò là "Tòa án tối cao" — lớp thanh toán tối hậu (*Settlement Layer*) có độ bảo mật cao nhất, thích hợp cho các tổ chức tài chính chuyển nhượng tài sản hàng chục triệu USD, không phù hợp cho người dùng phổ thông tiêu dùng hàng ngày.
2. **Layer 2 là tương lai của ứng dụng kinh tế số Web3:** Các giải pháp Rollup (Arbitrum, Optimism, Base) kế thừa trọn vẹn tính bảo mật của Layer 1 nhưng xử lý giao dịch off-chain, đưa chi phí mỗi giao dịch về dưới 0,05 USD, mở ra cánh cửa hiện thực hóa các bài toán thương mại điện tử, vé sự kiện, điểm thưởng và mạng xã hội Web3.
3. **Bài học cho sinh viên ngành Kinh tế:** Viết mã chạy được mới chỉ là điều kiện cần; giải được bài toán điểm hòa vốn và trải nghiệm người dùng về mặt chi phí mới là điều kiện đủ để một sản phẩm công nghệ tồn tại trên thị trường.

---

## 7. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao lab 7 - tinh chi phi van hanh thuc te tren L1 va L2"
git push
```
