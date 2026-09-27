# BÁO CÁO THỰC HÀNH — LAB 7: TÍNH CHI PHÍ VẬN HÀNH THỰC TẾ

**Môn học:** Kinh tế số / Web3 Starter (ECO2432)  
**Chủ đề:** LAB 7 — Tính chi phí vận hành thực tế  
**Thời lượng:** 75 phút · **Hình thức:** Nhóm 2 người  
**Sản phẩm nộp quy định:** `lab07.md` gồm bảng tính và một đoạn kết luận về tính khả thi  

---

## 1. Thông tin chung
- **Họ và tên sinh viên thực hiện:** Ngo Thi Thuy Van
- **Mã sinh viên:** 23K4300023
- **Lớp:** K57 - Kinh tế số
- **Địa chỉ ví cá nhân (Student Wallet):** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Địa chỉ ví bạn ghép cặp (Partner Wallet):** `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`
- **Tệp báo cáo:** [`Lab 1-7/lab07.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/lab07.md)

---

## 2. Gắn với công việc thực tế (Ý nghĩa kinh tế của bài Lab)

> *"Đây là bài toán kinh tế, không phải bài toán kỹ thuật — và là phần sinh viên Kinh tế làm tốt hơn sinh viên CNTT. Một sản phẩm chạy được nhưng chi phí giao dịch cao hơn giá trị giao dịch thì không có mô hình kinh doanh."*

Trong phát triển giải pháp kinh tế số và Web3, một hợp đồng thông minh dù được lập trình hoàn hảo và bảo mật tuyệt đối vẫn sẽ bị thị trường đào thải nếu không vượt qua được bài toán **Kinh tế vi mô trên từng đơn vị sản phẩm (Unit Economics)**. 

Vai trò của Chuyên viên Kinh tế số và Chuyên viên Phân tích Nghiệp vụ (Business Analyst - BA) là:
1. **Dự báo chi phí hạ tầng (Gas Overhead Forecasting):** Tính toán chính xác định phí và biến phí vận hành blockchain trước khi ký quyết định triển khai.
2. **Thiết kế cơ chế phân bổ chi phí (Cost Allocation Strategy):** Xác định rõ ai là người chịu phí (Doanh nghiệp, CLB hay Khách hàng)? Phí đó có triệt tiêu động lực sử dụng của khách hàng hay không?
3. **Lựa chọn kiến trúc mạng tối ưu:** Xác định ranh giới hiệu quả giữa mạng Lớp 1 (Layer 1 - Ethereum Mainnet) và mạng Lớp 2 (Layer 2 Rollups như Arbitrum, Optimism, Base).

---

## 3. Bước 1 — Cấu trúc phí giao dịch trên mạng Ethereum (20 phút)

### 3.1. Công thức nền tảng
Chi phí của một giao dịch on-chain được cấu thành bởi hai yếu tố:
$$\text{Phí một giao dịch} = \text{Lượng gas tiêu thụ (Gas Used)} \times \text{Đơn giá gas (Gas Price)}$$

- **Đơn vị đo lường:**
  + $1\text{ Gwei} = 10^{-9}\text{ ETH} = 0,000000001\text{ ETH}$.
  + $\text{Chi phí giao dịch (ETH)} = \text{Gas tiêu thụ} \times \text{Đơn giá gas (Gwei)} \times 10^{-9}$.
  + $\text{Chi phí giao dịch (USD)} = \text{Chi phí giao dịch (ETH)} \times \text{Giá ETH (USD)}$.

### 3.2. Bảng tham khảo mức tiêu thụ Gas theo loại thao tác EVM
Dưới đây là các mốc tiêu thụ gas định mức theo tài liệu kỹ thuật của máy ảo Ethereum (EVM):

| STT | Loại thao tác | Lượng gas tham khảo | Bản chất kỹ thuật trên EVM |
| :-: | :--- | :---: | :--- |
| 1 | **Chuyển ETH thông thường** | `21.000` | Mức gas cơ sở tối thiểu cho mọi giao dịch thanh toán cơ bản giữa hai tài khoản EOA. |
| 2 | **Chuyển token theo chuẩn ERC-20** | `~50.000 – 65.000` | Gọi hàm `transfer()`, đọc và ghi lại số dư của 2 tài khoản trong mapping lưu trữ. |
| 3 | **Ghi một biến mới vào bộ nhớ lâu dài (`SSTORE`)** | `~20.000` | Ghi ô nhớ từ giá trị `0` sang giá trị khác `0` (chiếm dụng tài nguyên lưu trữ vĩnh viễn của các validator node). |
| 4 | **Sửa một biến đã có trong bộ nhớ (`SSTORE`)** | `~5.000` | Thay đổi ô nhớ đã có sẵn dữ liệu khác `0` sang một giá trị mới (tốn ít tài nguyên hơn ghi mới). |
| 5 | **Triển khai hợp đồng cỡ nhỏ (Deploy)** | `~500.000 – 1.500.000` | Lưu trữ toàn bộ bytecode của hợp đồng lên blockchain và thực thi hàm `constructor`. |

> **Lưu ý nghiệp vụ:** Con số thực tế thay đổi theo mã nguồn cụ thể của từng hợp đồng. Sinh viên sẽ **tự đo lường bằng Remix IDE ở Lab 9** để thu thập số liệu thực nghiệm chính xác.

---

## 4. Bước 2 — Giải bài toán: Thẻ tích điểm Câu lạc bộ Sinh viên (35 phút)

### 4.1. Dữ liệu đề bài
- **Mô hình hoạt động:** Câu lạc bộ sinh viên phát hành thẻ tích điểm trên blockchain.
- **Tần suất vận hành:** Mỗi tháng có **1.000 lượt cộng điểm**.
- **Bản chất kỹ thuật:** Mỗi lượt là một giao dịch ghi dữ liệu vào hợp đồng thông minh (thao tác ghi dữ liệu định mức: `20.000` gas; nếu tính toàn bộ hàm giao dịch smart contract thực tế kèm logic kiểm tra là `~45.000` gas).
- **Các tham số giả định:**
  + Đơn giá gas: **20 Gwei** ($20 \times 10^{-9}\text{ ETH}$).
  + Giá ETH thị trường: **3.000 USD/ETH**.
  + Tỷ giá quy đổi tham khảo: $1\text{ USD} \approx 25.400\text{ VNĐ}$.

---

### 4.2. Trả lời chi tiết từng câu hỏi đề bài

#### a. Với đơn giá gas 20 Gwei và giá ETH 3.000 USD, chi phí một tháng là bao nhiêu USD?

**Phương pháp tính:**
1. **Lượng gas cho một lượt cộng điểm:** $G = 20.000\text{ gas}$ (theo mốc thao tác ghi dữ liệu `SSTORE`).
2. **Chi phí một lượt cộng điểm bằng ETH:**
   $$\text{Fee}_{\text{1 tx (ETH)}} = 20.000 \times 20 \times 10^{-9} = 0,0004\text{ ETH}$$
3. **Chi phí một lượt cộng điểm bằng USD:**
   $$\text{Fee}_{\text{1 tx (USD)}} = 0,0004\text{ ETH} \times 3.000\text{ USD/ETH} = 1,20\text{ USD} \quad (\approx 30.480\text{ VNĐ})$$
4. **Tổng chi phí vận hành một tháng cho 1.000 lượt:**
   $$\text{Chi phí tháng}_{\text{Layer 1}} = 1.000 \times 1,20\text{ USD} = \mathbf{1.200\text{ USD/tháng}} \quad (\mathbf{\approx 30.480.000\text{ VNĐ/tháng}})$$

*(Mở rộng: Nếu tính theo hàm smart contract tích điểm đầy đủ tiêu thụ 45.000 gas, chi phí cho mỗi lượt là $2,70\text{ USD}$, tương ứng tổng chi phí hàng tháng lên tới **2.700 USD/tháng**, xấp xỉ **68.580.000 VNĐ/tháng**).*

---

#### b. Nếu chuyển sang mạng Layer 2 với đơn giá rẻ hơn khoảng 100 lần, chi phí còn bao nhiêu?

**Phương pháp tính:**
Các giải pháp Layer 2 (Arbitrum, Optimism, Base) sử dụng công nghệ gom giao dịch (*Rollup*) và cơ chế nén dữ liệu blob theo bản nâng cấp EIP-4844, giúp giảm đơn giá phí trung bình khoảng **100 lần** so với mạng gốc Layer 1:
1. **Chi phí một lượt cộng điểm trên Layer 2:**
   $$\text{Fee}_{\text{1 tx (L2)}} = \frac{1,20\text{ USD}}{100} = \mathbf{0,012\text{ USD}} \quad (\approx 305\text{ VNĐ})$$
2. **Tổng chi phí vận hành một tháng cho 1.000 lượt:**
   $$\text{Chi phí tháng}_{\text{Layer 2}} = \frac{1.200\text{ USD}}{100} = \mathbf{12\text{ USD/tháng}} \quad (\mathbf{\approx 304.800\text{ VNĐ/tháng}})$$

*(Mở rộng: Với hàm đầy đủ 45.000 gas, chi phí trên L2 là **0,027 USD/lượt**, tổng chi phí là **27 USD/tháng**, tương đương **685.800 VNĐ/tháng**).*

---

#### c. Ai trả khoản này — câu lạc bộ hay sinh viên? Nếu sinh viên trả, họ có chấp nhận không?

Dưới góc nhìn kinh tế học hành vi và tài chính vi mô:

##### Kịch bản 1: Câu lạc bộ chi trả toàn bộ phí vận hành
- **Trên Layer 1 (1.200 USD $\approx$ 30,5 triệu VNĐ/tháng):**
  + **Bất khả thi tuyệt đối:** Ngân sách hoạt động thường niên của một câu lạc bộ sinh viên trường Đại học thường chỉ dao động trong khoảng từ **5.000.000 đến 15.000.000 VNĐ cho cả một năm học**. Chi phí gas on-chain trên Layer 1 trong 1 tháng đã gấp từ 2 đến 6 lần ngân sách của cả năm. CLB sẽ rơi vào tình trạng vỡ nợ và dừng hoạt động ngay trong tuần đầu tiên.
- **Trên Layer 2 (12 USD $\approx$ 305.000 VNĐ/tháng):**
  + **Hoàn toàn khả thi:** Số tiền xấp xỉ 300.000 VNĐ/tháng chỉ tương đương vài ly trà sữa hoặc một phần rất nhỏ trích từ quỹ thành viên / nguồn tài trợ sự kiện. CLB hoàn toàn có khả năng thanh toán.
  + Hơn thế nữa, CLB có thể triển khai cơ chế **Account Abstraction (ERC-4337 / Paymaster)** để tự động đứng ra bảo lãnh và tài trợ phí gas cho sinh viên. Sinh viên không cần sở hữu ví phức tạp hay giữ đồng ETH nào vẫn được tích điểm mượt mà.

##### Kịch bản 2: Sinh viên (người tham gia tích điểm) tự chi trả phí
- **Trên Layer 1 (Sinh viên trả 1,20 USD $\approx$ 30.500 VNĐ cho mỗi lần nhận điểm):**
  + **Sinh viên chắc chắn từ chối 100%:** Một điểm thưởng tham gia hoạt động của CLB sinh viên thường chỉ có giá trị quy đổi tượng trưng: một vé gửi xe miễn phí (5.000 VNĐ), một cuốn sổ tay nhỏ (10.000 VNĐ) hoặc mã giảm giá đồ uống (15.000 VNĐ). Bắt sinh viên chi trả **30.500 VNĐ tiền phí gas** để nhận về một phần thưởng trị giá 10.000 VNĐ là một quyết định hoàn toàn phi lý trí về mặt tài chính. Không một sinh viên nào chấp nhận dùng ứng dụng này.
- **Trên Layer 2 (Sinh viên trả 0,012 USD $\approx$ 305 VNĐ cho mỗi lần nhận điểm):**
  + Về mặt tài chính, mức phí 305 VNĐ là không đáng kể. 
  + Tuy nhiên, về mặt trải nghiệm người dùng (**UX Friction**), nếu bắt sinh viên tự trả phí thì vẫn **thất bại** vì rào cản thao tác quá lớn: Sinh viên phải cài đặt tiện ích ví MetaMask, phải thực hiện chuyển đổi mạng sang Layer 2, phải mua và chuyển ETH vào ví để làm phí gas, và phải nhấn xác nhận ký ví mỗi khi nhận điểm.
  + **Kết luận phương án trả phí tối ưu:** **Câu lạc bộ phải là bên chi trả khoản phí này thông qua Paymaster trên mạng Layer 2**. Điều này giúp tạo ra trải nghiệm "Gasless" (không phí), xóa bỏ hoàn toàn rào cản công nghệ cho sinh viên.

---

#### d. Bảng so sánh tổng hợp & Kết luận: Mô hình này khả thi trên mạng nào?

### BẢNG TÍNH SO SÁNH CHI PHÍ VẬN HÀNH: LAYER 1 VS LAYER 2

| Tiêu chí so sánh | Mạng Layer 1 (Ethereum Mainnet) | Mạng Layer 2 (Arbitrum / Optimism / Base) | Chênh lệch / Tác động kinh tế |
| :--- | :---: | :---: | :---: |
| **Đơn vị giao dịch** | 1.000 lượt cộng điểm / tháng | 1.000 lượt cộng điểm / tháng | Cùng quy mô vận hành |
| **Lượng gas tiêu thụ / lượt** | 20.000 gas | 20.000 gas | Thực thi tương đương |
| **Đơn giá gas hiệu dụng** | 20 Gwei | $\approx 0,2\text{ Gwei}$ (nhờ EIP-4844 Blob) | **Rẻ hơn 100 lần** |
| **Chi phí gas cho 1 lượt** | **1,20 USD** (30.480 VNĐ) | **0,012 USD** (305 VNĐ) | **Tiết kiệm 99% chi phí** |
| **Tổng chi phí 1 tháng (1.000 tx)** | **1.200 USD** (30.480.000 VNĐ) | **12 USD** (304.800 VNĐ) | **Giảm từ 30,5 triệu xuống 305 nghìn** |
| **Thời gian xác nhận giao dịch** | 12 – 15 giây (có thể nghẽn mạng) | $\approx 1 – 2\text{ giây}$ | Nhanh hơn gần 10 lần |
| **Khả năng CLB tài trợ chi phí** | ❌ **Không thể** (vượt ngân sách năm) | ✅ **Dễ dàng** (~300k VNĐ/tháng) | Đảm bảo tính bền vững tài chính |
| **Mức độ tiếp nhận của sinh viên** | ❌ **Từ chối tuyệt đối** (phí > thưởng) | ✅ **Ủng hộ cao** (trải nghiệm mượt) | Tăng trưởng người dùng thực tế |
| **KẾT LUẬN TÍNH KHẢ THI** | ⛔ **HOÀN TOÀN BẤT KHẢ THI** | 🟢 **HOÀN TOÀN KHẢ THI** | **Bắt buộc triển khai trên L2** |

> **KẾT LUẬN CẦN RÚT RA (SƯ PHẠM ECO2432):**  
> Câu hỏi (d) dẫn tự nhiên đến khái niệm **mạng Layer 2** — giải pháp mở rộng quy mô mang tính sống còn cho toàn bộ hệ sinh thái Web3, và là nội dung trọng tâm cần bổ sung vào **Session 02 về Mạng Lớp 2**.  
> Mạng Layer 1 chỉ đóng vai trò là tầng thanh toán tối hậu (*Settlement Layer*) có độ bảo mật cao nhất dành cho các giao dịch chuyển tiền lớn, còn mọi ứng dụng tiêu dùng hàng ngày (*Consumer Web3 Apps*) bắt buộc phải vận hành trên các mạng Layer 2.

---

## 5. Bước 3 — Mở rộng: Tính toán chi phí cho Đồ án nhóm ECO2432 (20 phút)

Nhóm sinh viên áp dụng đúng khung tính toán kinh tế ở trên để thẩm định tính khả thi cho ý tưởng đồ án môn học đang xây dựng:

### 5.1. Ý tưởng đồ án: Nền tảng Ký quỹ Mua bán Đồ dùng Sinh viên (`CampusEscrow`)
- **Mục tiêu sản phẩm:** Giải quyết vấn nạn lừa đảo khi sinh viên mua bán máy tính, điện thoại cũ, giáo trình học tập và đồ gia dụng ký túc xá qua mạng xã hội (tình trạng chuyển tiền cọc nhưng bị chặn tin nhắn).
- **Quy mô dự kiến ban đầu:** **200 giao dịch thành công / tháng**.
- **Giá trị trung bình một đơn hàng:** 200.000 VNĐ / đơn.

### 5.2. Phân rã chuỗi giao dịch on-chain của một đơn hàng ký quỹ hoàn chỉnh
Một quy trình ký quỹ mua bán minh bạch trên smart contract bao gồm 3 thao tác chính:
1. `createAndDeposit()`: Người mua khởi tạo đơn và nạp tiền thanh toán vào hợp đồng giữ hộ ($\approx 55.000\text{ gas}$).
2. `confirmReceived()`: Người mua xác nhận đã nhận đúng đồ, giải ngân tiền cọc cho người bán ($\approx 35.000\text{ gas}$).
3. `resolveDispute() / refund()`: Dự phòng xử lý khiếu nại hoặc hủy đơn hoàn tiền (tỷ lệ ước tính 10% số ca, trung bình $\approx 10.000\text{ gas}$ phân bổ trên mỗi đơn).
$\rightarrow$ **Tổng lượng gas tiêu thụ trung bình cho 1 chu trình đơn hàng hoàn tất:** $G = \mathbf{100.000\text{ gas}}$.

---

### 5.3. Bảng dự toán chi phí và phân tích hòa vốn (L1 vs L2)

| Chỉ số tài chính & kỹ thuật | Đơn vị | Kịch bản Layer 1 (Ethereum Mainnet) | Kịch bản Layer 2 (Base / Arbitrum) | Đánh giá nghiệp vụ kinh tế |
| :--- | :---: | :---: | :---: | :--- |
| **Quy mô đơn hàng / tháng** | Đơn | 200 | 200 | Quy mô thử nghiệm KTX |
| **Lượng gas trung bình / đơn** | Gas | 100.000 | 100.000 | Đầy đủ chu trình ký quỹ |
| **Đơn giá gas giả định** | Gwei | 20 Gwei | 0,2 Gwei | L2 rẻ hơn 100 lần |
| **Chi phí gas cho 1 đơn hàng** | USD (VNĐ) | **6,00 USD** (152.400 VNĐ) | **0,06 USD** (1.524 VNĐ) | Phí trên L1 chiếm trọn giá trị đơn |
| **Giá trị đơn hàng trung bình** | VNĐ | 200.000 VNĐ | 200.000 VNĐ | Hàng hóa sinh viên đã qua sử dụng |
| **Tỷ lệ phí gas / Giá trị đơn** | % | **76,2%** | **0,76%** | Mức < 1% là cực kỳ lý tưởng |
| **Tổng chi phí gas 200 đơn / tháng**| USD (VNĐ) | **1.200 USD** (30.480.000 đ) | **12 USD** (304.800 đ) | L1 vượt sức chịu đựng của dự án |
| **Mô hình thu phí sàn đề xuất** | % giá trị đơn | Không thể thu phí vì gas quá đắt | Thu phí dịch vụ **1,5%** (= 3.000 đ/đơn) | Sinh viên sẵn sàng trả 3.000 đ để an toàn |
| **Doanh thu phí sàn (200 đơn)** | VNĐ | 0 VNĐ | $200 \times 3.000 = 600.000\text{ VNĐ}$ | Nguồn thu ròng của nhóm |
| **Lợi nhuận ròng sau chi phí gas** | VNĐ | Âm 30.480.000 VNĐ (Lỗ nặng) | **+295.200 VNĐ / tháng** (Dương) | Dự án có dòng tiền thặng dư ngay lập tức |
| **KẾT LUẬN KHẢ THI ĐỒ ÁN** | Kết luận | ⛔ **Thất bại hoàn toàn** | 🟢 **Mô hình kinh doanh khả thi 100%** | **Chọn triển khai trên mạng Layer 2** |

---

## 6. Tổng kết bài học nghiệp vụ (Dành cho Chuyên viên Kinh tế số)

1. **Hiểu rõ ranh giới giữa Khả thi Kỹ thuật và Khả thi Kinh tế:**  
   Việc viết mã và chạy thử thành công một smart contract chỉ chiếm 30% chặng đường phát triển sản phẩm. 70% còn lại quyết định sự sống còn của dự án nằm ở **Unit Economics** (Chi phí trên mỗi đơn vị dịch vụ phải nhỏ hơn rất nhiều so với Giá trị thặng dư mang lại cho khách hàng).
2. **Layer 1 và Layer 2 giải quyết hai bài toán kinh tế khác nhau:**
   - **Layer 1 (Ethereum Mainnet):** Đóng vai trò là hạ tầng tài chính nền móng (*Settlement Layer*), ưu tiên tối thượng tính phân tán và bảo mật tuyệt đối, phù hợp với các giao dịch chuyển tài sản giá trị hàng triệu USD của các định chế tài chính lớn.
   - **Layer 2 (Arbitrum, Base, Optimism):** Đóng vai trò là tầng thực thi mở rộng (*Execution Layer*), gom hàng ngàn giao dịch lại và ghi nhận dữ liệu nén về L1, giúp hạ phí xuống mức vài trăm đồng và tốc độ giao dịch tức thì, là nền tảng bắt buộc cho các ứng dụng tiêu dùng đại chúng (Thương mại điện tử, Ký quỹ, Điểm thưởng, Vé sự kiện Web3).
3. **Cơ chế Account Abstraction là chìa khóa thâm nhập thị trường:**  
   Để người dùng phổ thông (không rành công nghệ) tiếp cận Web3, doanh nghiệp cần kết hợp mạng Layer 2 với hợp đồng bảo lãnh phí (**Paymaster**). Điều này cho phép người dùng đăng nhập bằng Google/Email và thực hiện giao dịch hoàn toàn miễn phí, trong khi doanh nghiệp bù đắp chi phí đó qua các mô hình kiếm tiền truyền thống (hoa hồng, quảng cáo, tài trợ).

---

## 7. Nhật ký lệnh Git đã thực thi
```bash
git add .
git commit -m "docs: hoan thanh bao cao lab 7 - tinh chi phi van hanh thuc te tren L1 va L2 theo chuan ECO2432"
git push
```
