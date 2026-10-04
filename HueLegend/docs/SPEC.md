# SPEC — ĐẶC TẢ NGHIỆP VỤ HỆ THỐNG TRUY XUẤT ĐẶC SẢN HUẾ (HUELEGEND v0.2)

## 1. Mục đích
Hệ thống **HueLegend** ứng dụng công nghệ Blockchain (Ethereum Sepolia) nhằm minh bạch hóa toàn diện chuỗi cung ứng các đặc sản truyền thống xứ Huế (Mè xửng, Tôm chua, Trà Cung đình, Tinh dầu tràm, Nón bài thơ). Hệ thống cung cấp cơ chế lưu trữ lịch sử bất biến on-chain giúp bảo vệ uy tín các làng nghề OCOP và trao quyền cho người tiêu dùng tự kiểm chứng nguồn gốc sản phẩm qua mã QR.

---

## 2. Người dùng và Đối tượng thụ hưởng (Actors)
- **Cơ sở sản xuất (`ROLE_PRODUCER`):** Hộ sản xuất, hợp tác xã làng nghề Huế (ví dụ: Mè xửng Thiên Hương, Tôm chua Trọng Tín,...).
- **Đơn vị vận chuyển (`ROLE_LOGISTICS`):** Đơn vị giao vận đường bộ, đường sắt (Ga Huế), hàng không (Sân bay Phú Bài).
- **Đại lý / Cửa hàng bán lẻ (`ROLE_RETAILER`):** Điểm bán quà lưu niệm, siêu thị đặc sản tại Huế, Hà Nội, TP.HCM.
- **Cơ quan kiểm định (`ROLE_INSPECTOR`):** Chi cục Quản lý Chất lượng Nông Lâm Thủy sản TT Huế, Ban quản lý OCOP.
- **Khách mua hàng (Người dùng phổ thông / Consumer):** Du khách, người tiêu dùng quét mã QR tra cứu miễn phí.

---

## 3. Đầu vào và Đầu ra

### 3.1. Dữ liệu đầu vào
- Mã định danh lô hàng (`batchCode`): chuỗi ký tự duy nhất (ví dụ: `HL-MEXUNG-2026-001`).
- Tên đặc sản (`productName`): tên sản phẩm làng nghề được bảo hộ.
- Vùng nguyên liệu (`origin`): địa danh xuất xứ nguyên liệu sạch tại Thừa Thiên Huế.
- Thông tin chặng: địa điểm (`location`), hành động thực hiện (`action`), đường dẫn chứng từ kiểm định (`metadataURI`).
- Tiền nạp ký quỹ bảo đảm uy tín làng nghề (`msg.value`).
- Chữ ký xác thực của ví Web3 gửi giao dịch (`msg.sender`).

### 3.2. Dữ liệu đầu ra
- Lịch sử chuỗi cung ứng bất biến dạng dòng thời gian (Timeline) bao gồm: thời gian khối, người ký, vai trò, địa điểm, hành động, mã băm giao dịch (TxHash).
- Mã phản hồi nhanh (QR Code) động liên kết trực tiếp đến trang tra cứu lô hàng.
- Trạng thái kiểm định OCOP (`isVerified`: `true`/`false`).
- Số dư tiền ký quỹ và thời gian mở khóa cọc của cơ sở sản xuất.

---

## 4. Bốn quy tắc nghiệp vụ chuỗi cung ứng cốt lõi (Core Supply Chain Rules)

### Quy tắc 1 (Khởi tạo lô đặc sản - Batch Creation)
- **Ai được làm gì:** Chỉ địa chỉ ví được cấp quyền `ROLE_PRODUCER` (hoặc `owner`) mới được gọi hàm `createBatch`.
- **Khi nào:** Khi sản phẩm hoàn thành chế biến tại xưởng và chuẩn bị đóng gói dán tem.
- **Giới hạn bao nhiêu:** Mỗi mã lô (`batchCode`) là chuỗi không rỗng và chỉ được tạo duy nhất một lần trên toàn mạng lưới (`batchCode` không được trùng lặp).
- **Lỗi thì sao:** 
  - Nếu không có quyền $\rightarrow$ Revert `UnauthorizedCaller(msg.sender, ROLE_PRODUCER)`.
  - Nếu mã lô đã tồn tại $\rightarrow$ Revert `BatchAlreadyExists(batchCode)`.
  - Nếu để trống thông tin $\rightarrow$ Revert `EmptyString(fieldName)`.

### Quy tắc 2 (Thêm chặng theo đúng vai - Role-based Checkpoint)
- **Ai được làm gì:** Địa chỉ ví nắm giữ đúng vai trò `role` được khai báo (`ROLE_LOGISTICS`, `ROLE_RETAILER`, `ROLE_INSPECTOR`, `ROLE_PRODUCER`) mới được gọi `addCheckpoint`.
- **Khi nào:** Khi lô hàng được tiếp nhận, chuyển giao, lưu kho hoặc kiểm tra điều kiện bảo quản tại một địa điểm mới.
- **Giới hạn bao nhiêu:** Lô hàng mục tiêu phải đang tồn tại trên chuỗi (`exists == true`). Mỗi giao dịch ghi nhận đúng 1 chặng kèm chữ ký ví của người gửi.
- **Lỗi thì sao:**
  - Nếu mã lô không tồn tại $\rightarrow$ Revert `BatchNotFound(batchCode)`.
  - Nếu ví gửi giao dịch không sở hữu vai trò tương ứng $\rightarrow$ Revert `UnauthorizedCaller(msg.sender, role)`.

### Quy tắc 3 (Thẩm định và Cấp chứng nhận OCOP - Inspection Verification)
- **Ai được làm gì:** Chỉ cơ quan kiểm định độc lập nắm giữ vai trò `ROLE_INSPECTOR` mới được gọi hàm `verifyBatch`.
- **Khi nào:** Sau khi tiến hành lấy mẫu kiểm nghiệm vi sinh, vệ sinh ATVSTP và thẩm định hồ sơ làng nghề đạt chuẩn.
- **Giới hạn bao nhiêu:** Chỉ thực hiện trên lô hàng đã tồn tại. Cờ `isVerified` được chuyển sang `true` và tự động ghi nhận chặng kiểm định có gắn link chứng chỉ IPFS.
- **Lỗi thì sao:** Nếu ví không phải là `ROLE_INSPECTOR` $\rightarrow$ Revert `UnauthorizedCaller(msg.sender, ROLE_INSPECTOR)`.

### Quy tắc 4 (Tra cứu và Quét mã QR - Public Free Traceability)
- **Ai được làm gì:** Bất kỳ ai (Khách du lịch, người tiêu dùng, thanh tra thị trường) đều có thể gọi các hàm truy vấn `getBatch` và `getCheckpoints`.
- **Khi nào:** Bất kỳ lúc nào, thông qua trình duyệt hoặc quét camera mã QR trên bao bì sản phẩm.
- **Giới hạn bao nhiêu:** Không giới hạn số lần truy vấn, không yêu cầu người dùng phải sở hữu ví Web3 hay có số dư ETH (hàm `view` đọc dữ liệu off-chain hoàn toàn miễn phí gas).
- **Lỗi thì sao:** Nếu nhập mã lô không tồn tại $\rightarrow$ Revert `BatchNotFound(batchCode)`.

---

## 5. Đặc tả mô hình Két Ký quỹ Khóa thời gian (Áp dụng từ Lab 9 TimeLockVault)

Học phần Lab 9 cung cấp nền tảng **Két tiết kiệm có khóa thời gian (`TimeLockVault`)** — mô hình ký gửi có điều kiện, nền móng của cơ chế giữ hộ tiền cọc bảo đảm chất lượng của làng nghề trong HueLegend.

### 5.1. Năm quy tắc chuẩn của Két khóa thời gian (TimeLockVault Rules)
- **R-TL1:** Ai cũng nạp được tiền vào két (`deposit() payable`).
- **R-TL2:** Chỉ người tạo két (`owner`) mới có quyền rút tiền (`withdraw()`).
- **R-TL3:** Chỉ rút được tiền khi thời điểm hiện tại của block đã qua mốc mở khóa (`block.timestamp >= unlockTime`).
- **R-TL4:** Số tiền nạp vào két phải lớn hơn 0 (`msg.value > 0`), nạp 0 sẽ bị từ chối với lỗi `ZeroAmount()`.
- **R-TL5:** Mọi lần nạp và rút tiền đều phải phát sự kiện (`Deposited`, `Withdrawn`) có đánh dấu `indexed` để phục vụ tra cứu minh bạch.

### 5.2. Chuyển giao kỹ thuật vào luồng cốt lõi của HueLegend (`ProjectCore.sol`)
Trong dự án HueLegend, nhóm chuyển giao trọn vẹn 4 kỹ thuật cốt lõi vừa học vào chức năng **Ký quỹ bảo đảm uy tín làng nghề (Reputation Staking with TimeLock)**:
1. **Phân quyền chặt chẽ:** Chỉ ví sở hữu `ROLE_PRODUCER` nộp tiền cọc và chỉ chính ví đó mới được rút cọc khi hết hạn.
2. **Sự kiện minh bạch:** Phát `StakeDeposited(producer, amount, unlockTime)` và `StakeWithdrawn(producer, amount)`.
3. **Lỗi tùy biến (Custom Errors):** `StakeTooLow()`, `StillLocked(unlockAt, currentTime)`, `NothingToWithdraw()`, `TransferFailed()`.
4. **Quy trình Checks — Effects — Interactions (CEI):** Kiểm tra điều kiện thời gian trước $\rightarrow$ Xóa số dư cọc về 0 $\rightarrow$ Phát sự kiện $\rightarrow$ Chuyển ETH ra ngoài bằng `call{value: ...}("")`.
