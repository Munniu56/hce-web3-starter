# ECONOMIC_RULES — QUY TẮC KINH TẾ, QUYỀN LỢI VÀ QUẢN TRỊ DỰ ÁN HUELEGEND

Tài liệu này xác lập mô hình kinh tế số (Tokenomics / Economic Model), cơ chế phí, ký quỹ bảo đảm và chế tài xử lý gian lận trong mạng lưới truy xuất nguồn gốc đặc sản Huế **HueLegend**.

---

## 1. Nguyên tắc thiết kế kinh tế
- **Minh bạch và công bằng:** Chi phí duy trì hệ thống được chia sẻ hợp lý giữa các cơ sở sản xuất và đơn vị phân phối; người tiêu dùng được tra cứu hoàn toàn miễn phí.
- **Quy chuẩn tỷ lệ:** Toàn bộ tỷ lệ phần trăm được tính toán theo đơn vị **Basis Point (bps)**, trong đó $1\% = 100\text{ bps}$, $100\% = 10.000\text{ bps}$.
- **Ràng buộc trách nhiệm bằng ký quỹ:** Cơ sở sản xuất phải cam kết chất lượng thông qua khoản đặt cọc bảo đảm uy tín (Reputation Stake).

---

## 2. Các tham số kinh tế trong hệ thống

| Tham số | Giá trị đề xuất | Đơn vị quy chuẩn | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **Phí tạo lô hàng (`batchCreationFee`)** | `0.001` ETH (~2-3 USD) | Wei / ETH | Bù đắp chi phí lưu trữ dữ liệu vĩnh viễn trên blockchain và tài trợ quỹ vận hành mạng lưới. |
| **Tiền ký quỹ cơ sở (`producerStake`)** | `0.05` ETH | Wei / ETH | Khoản đặt cọc duy trì quyền `ROLE_PRODUCER`; bị tịch thu nếu phát hiện làm giả nguồn gốc. |
| **Tỷ lệ thưởng người báo cáo gian lận (`bountyRateBps`)** | `5.000` bps (50%) | Basis point | Tỷ lệ tiền phạt trích thưởng cho khách hàng hoặc thanh tra chứng minh được hàng giả. |
| **Tỷ lệ nộp Quỹ phát triển OCOP Huế (`fundRateBps`)** | `5.000` bps (50%) | Basis point | Tỷ lệ tiền phạt nộp về Quỹ xúc tiến thương mại đặc sản làng nghề Huế. |
| **Phí tra cứu của khách hàng** | `0` ETH (Miễn phí) | ETH | Người tiêu dùng quét QR gọi hàm `view` miễn phí, không yêu cầu ví có số dư. |

---

## 3. Cơ chế phân bổ dòng tiền

1. **Khi Cơ sở sản xuất tạo lô hàng:**
   - Cơ sở gửi phí tạo lô hàng vào hợp đồng thông minh.
   - Khoản phí này được chuyển vào ví Quỹ phát triển Hệ thống (`ecosystemFund`) bằng phương thức an toàn `call{value: ...}("")`.
2. **Cơ chế Ký quỹ & Xử phạt Gian lận (Slashing Mechanism):**
   - **Ký quỹ ban đầu:** Khi được cấp quyền `ROLE_PRODUCER`, cơ sở nộp khoản cọc bảo đảm `producerStake`.
   - **Phát hiện gian lận:** Nếu cơ sở sản xuất khai báo sai nguồn gốc (ví dụ: dùng mè/sen nhập lậu giá rẻ nhưng dán nhãn "Đặc sản Cung Đình Huế"), Ban thẩm định OCOP (`ROLE_INSPECTOR`) cùng Admin sẽ kích hoạt quyết định xử phạt (Slashing).
   - **Phân bổ tiền cọc bị tịch thu:**
     $$\text{Tiền phạt} = \text{producerStake}$$
     $$\text{Thưởng người tố giác} = \text{Tiền phạt} \times \frac{5.000}{10.000} = 50\%$$
     $$\text{Nộp Quỹ OCOP Huế} = \text{Tiền phạt} \times \frac{5.000}{10.000} = 50\%$$
   - Ngay lập tức, vai trò `ROLE_PRODUCER` của cơ sở vi phạm bị thu hồi (`revokeRole`), toàn bộ các lô hàng chưa xuất kho bị đánh dấu cảnh báo gian lận.

---

## 4. Quyền lợi của các bên tham gia

- **Cơ sở sản xuất chân chính:** Bảo vệ thương hiệu độc quyền, chứng minh nguồn gốc chuẩn chỉ trước người tiêu dùng cả nước và quốc tế, tăng giá trị thặng dư của sản phẩm.
- **Đơn vị Logistics & Điểm bán lẻ:** Minh bạch trách nhiệm lưu kho và vận chuyển, tránh việc bị quy trách nhiệm oan uổng nếu hàng bị hỏng trước khi nhận bàn giao.
- **Khách mua hàng:** An tâm tuyệt đối về chất lượng đặc sản mua làm quà lưu niệm; có quyền giám sát và nhận thưởng xứng đáng khi phát hiện cơ sở mạo danh.

---

## 5. Cơ chế quản trị (Governance)

- Mọi tham số kinh tế (mức phí, tiền cọc, tỷ lệ basis point) đều có thể được cập nhật bởi Ban Quản trị thông qua hàm `updateEconomicParameters()` phát sự kiện minh bạch on-chain.
- Giới hạn an toàn: Mức phí tối đa không được vượt quá `0.01 ETH` để bảo đảm mọi hộ kinh doanh nhỏ lẻ tại làng nghề truyền thống Huế đều có thể tiếp cận công nghệ Web3.
