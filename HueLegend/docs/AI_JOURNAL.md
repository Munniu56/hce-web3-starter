# AI_JOURNAL — NHẬT KÝ SỬ DỤNG AI VÀ LỖI ĐÃ PHÁT HIỆN

Dự án: **HueLegend — Nền tảng Truy xuất Đặc sản Huế trên Blockchain**  
Học phần: **ECO2432 — Tiền điện tử & Hợp đồng thông minh**  
Trợ lý AI: **Antigravity IDE (Gemini 3.8 Flash)**

---

## 1. Phiên làm việc khởi tạo cấu trúc dự án & Đặc tả v0.1 (Lab 8)

### Câu lệnh (Prompt) đưa vào:
> *"Tạo cấu trúc dự án chuẩn Lab 8 cho dự án HueLegend về Truy xuất đặc sản Huế. Giải quyết bài toán cơ sở sản xuất và khách mua cần lịch sử lô hàng bất biến. Luồng cốt lõi demo: Tạo lô -> thêm chặng bởi đúng vai -> quét QR xem lịch sử. Tuân thủ tuyệt đối AGENTS.md (Solidity ^0.8.20, CEI, custom error, event, chú thích không dấu, tối thiểu 3 test case gồm ca gian lận)."*

---

## 2. Thực hiện phản biện theo yêu cầu Bước 4 (Lab 8)

Nhóm đã sử dụng prompt chuẩn được quy định trong tài liệu Lab 8 để yêu cầu AI đóng vai người dùng thận trọng phản biện hệ thống:

### Prompt phản biện:
> *"Bạn là người dùng thận trọng. Chỉ dựa trên SPEC và ECONOMIC_RULES dưới đây, hãy nêu 5 cách một người có thể lạm dụng quy tắc hoặc làm người khác bị thiệt. Với mỗi cách, chỉ rõ quy tắc nào chưa đủ chặt. Không viết mã."*

### Kết quả phản biện của AI và Phản hồi/Biện pháp khắc phục của Nhóm:

#### 1. Lạm dụng 1: Nhân bản mã QR dán lên hàng giả (QR Code Replication / Sybil Physical Attack)
- **Hành vi lạm dụng:** Cơ sở sản xuất chỉ tạo 01 lô hàng thật gồm 100 hộp mè xửng on-chain, nhưng in hàng chục nghìn tem QR đó dán lên các sản phẩm làm giả, trôi nổi ngoài thị trường. Khách hàng quét mã QR vẫn thấy dữ liệu on-chain chuẩn chỉ.
- **Quy tắc chưa đủ chặt:** Quy tắc 1 trong `SPEC.md` chỉ quản lý tính duy nhất của mã lô `batchCode`, chưa ràng buộc số lượng đơn vị sản phẩm bán ra thực tế gắn liền với mã lô đó.
- **Biện pháp của Nhóm:** Nhóm sửa quy tắc trong `ECONOMIC_RULES.md` mục 4: Đề xuất triển khai giải pháp **QR kép** (01 mã QR công khai để tra cứu hành trình lô hàng + 01 mã cào phủ bạc chứa Serial Hash ngẫu nhiên bên trong hộp dùng một lần. Khi khách hàng cào xác nhận mua trên DApp, mã Serial bị vô hiệu hóa; nếu quét mã đã cào trước đó, hệ thống sẽ cảnh báo đỏ nguy cơ hàng giả mạo).

#### 2. Lạm dụng 2: Tống tiền hoặc cố tình không ký nhận chặng (Logistics Griefing Attack)
- **Hành vi lạm dụng:** Đơn vị vận chuyển sau khi nhận hàng từ xưởng mè xửng tại Huế cố tình không gọi hàm `addCheckpoint` để vòi vĩnh thêm chi phí từ cơ sở sản xuất, khiến lô hàng bị treo trạng thái trên DApp.
- **Quy tắc chưa đủ chặt:** Quy tắc 2 trong `SPEC.md` cho phép ví có `ROLE_LOGISTICS` thêm chặng nhưng chưa quy định cơ chế xử lý quá hạn (timeout) hoặc quyền chuyển giao chặng khẩn cấp.
- **Biện pháp của Nhóm:** Nhóm sửa quy tắc: Bổ sung cơ chế *Cập nhật chặng khẩn cấp (Emergency Checkpoint)*. Sau 48 giờ kể từ chặng xuất xưởng nếu đơn vị vận chuyển không ký xác thực, Cơ sở sản xuất có quyền đính kèm biên bản giao nhận ngoại vi để đẩy chặng tiếp theo và kích hoạt chế tài trừ điểm uy tín đơn vị vận chuyển.

#### 3. Lạm dụng 3: Vu khống và khiếu nại bừa bãi để nhận thưởng Bounty (False Accusation Exploit)
- **Hành vi lạm dụng:** Kẻ xấu liên tục gửi các báo cáo gian lận nhắm vào các cơ sở sản xuất uy tín nhằm gây nghẽn quy trình thẩm định hoặc câu kết trục lợi 50% tiền ký quỹ.
- **Quy tắc chưa đủ chặt:** Mục 1 trong `ECONOMIC_RULES.md` quy định thưởng 50% tiền cọc cho người tố giác nhưng chưa có chế tài ràng buộc nếu người tố giác khai báo sai sự thật.
- **Biện pháp của Nhóm:** Nhóm bổ sung quy tắc *Ký quỹ khiếu nại (Challenging Stake)* tại Mục 2 `ECONOMIC_RULES.md`: Người gửi đơn tố giác phải ký quỹ `0.01 ETH`. Nếu tố cáo chính xác, nhận lại cọc + thưởng 50% tiền phạt; nếu vu khống sai sự thật, tiền cọc bị tịch thu vào Quỹ OCOP.

#### 4. Lạm dụng 4: Nguy cơ Quản trị viên lạm quyền (Admin Rugpull & Centralization)
- **Hành vi lạm dụng:** Địa chỉ ví `owner` tùy tiện gọi `revokeRole` hoặc kích hoạt lệnh tịch thu tiền ký quỹ của cơ sở sản xuất mà không có sự đồng thuận của cơ quan chức năng.
- **Quy tắc chưa đủ chặt:** Mục 3 trong `ECONOMIC_RULES.md` trao toàn quyền quyết định cho `ROLE_ADMIN` mà chưa áp dụng cơ chế đa chữ ký (Multi-Signature).
- **Phản hồi của Nhóm (Chấp nhận rủi ro có lộ trình):** Trong khuôn khổ **Lab 8**, nhóm chấp nhận dùng một ví Admin để đơn giản hóa quá trình khởi tạo cấu trúc và kiểm thử cục bộ. Nhóm cam kết từ **Lab 11** sẽ nâng cấp lên hợp đồng đa chữ ký (Multi-Sig 2/3 giữa Ban quản lý OCOP, Đại diện làng nghề và Trưởng nhóm kỹ thuật) để kiểm soát việc tịch thu cọc.

#### 5. Lạm dụng 5: Đùn đẩy trách nhiệm khi hàng hóa hư hỏng trong quá trình vận chuyển (Blame Shifting)
- **Hành vi lạm dụng:** Sản phẩm tôm chua bị hỏng do xe vận chuyển tắt điều hòa, nhưng đơn vị vận chuyển đổ lỗi cho cơ sở sản xuất chế biến không đạt chuẩn, hoặc bên bán lẻ bảo quản sai cách.
- **Quy tắc chưa đủ chặt:** Quy tắc 2 chỉ ghi nhận văn bản mô tả chặng mà chưa ràng buộc tiêu chuẩn điều kiện vật lý lúc giao nhận.
- **Biện pháp của Nhóm:** Bổ sung yêu cầu tại Mục 4 `ECONOMIC_RULES.md`: Khi bên bán lẻ (`ROLE_RETAILER`) tiếp nhận hàng, bắt buộc phải chụp ảnh tình trạng niêm phong và ghi chú tình trạng vật lý vào `metadataURI`. Nếu bao bì rách/hỏng trước khi ký nhận, điểm bán từ chối chặng và trách nhiệm thuộc về bên vận chuyển.

---

## 3. Các lỗi kỹ thuật trong mã nguồn được phát hiện và khắc phục (Lab 8)

1. **Lỗi mạo danh vai trò (Role Impersonation):** Ban đầu hàm `addCheckpoint` chỉ nhận chuỗi tên vai trò mà không kiểm tra `msg.sender` có quyền hay không. Nhóm đã bổ sung hằng số `bytes32` (`ROLE_PRODUCER`, `ROLE_LOGISTICS`,...) và kiểm tra `_roles[msg.sender][role]` nghiêm ngặt.
2. **Lỗi tốn gas do revert string dài:** Đã chuyển toàn bộ sang Custom Errors của Solidity `^0.8.20` (`BatchAlreadyExists`, `UnauthorizedCaller`,...).
3. **Tuân thủ quy ước AGENTS.md:** Đã chuẩn hóa toàn bộ chú thích trong hợp đồng sang **tiếng Việt không dấu**.

---

## 4. Phiên làm việc Lab 9: Két tiết kiệm có khóa thời gian (TimeLockVault) & Áp dụng vào ProjectCore

### 4.1. Câu lệnh (Prompt) đưa vào theo yêu cầu Bước 2:
> *"Viết hợp đồng Solidity theo SPEC.md, tuân thủ AGENTS.md. Giải thích lựa chọn thiết kế trước khi đưa mã nguồn."*

### 4.2. Giải thích lựa chọn thiết kế kỹ thuật:
- **Tách bạch luồng Nạp (`deposit`) và Rút (`withdraw`):** Bất kỳ ai cũng nạp được tiền vào két (`external payable`), nhưng quyền rút chỉ dành riêng cho người tạo két (`owner`).
- **Khóa thời gian bằng `block.timestamp`:** Khởi tạo `unlockTime = block.timestamp + lockDurationSeconds`. Trước mốc thời gian này, hợp đồng từ chối mọi yêu cầu rút tiền với lỗi `StillLocked(unlockAt, currentTime)`.
- **Áp dụng mô hình Checks — Effects — Interactions (CEI):**
  1. *Checks:* Kiểm tra quyền sở hữu (`msg.sender == owner`), kiểm tra thời gian (`block.timestamp >= unlockTime`), kiểm tra số dư (`amount > 0`).
  2. *Effects:* Phát sự kiện `Withdrawn` và cập nhật trạng thái trước khi chuyển tiền ra ngoài.
  3. *Interactions:* Chuyển ETH bằng phương thức an toàn `(bool ok, ) = payable(owner).call{value: amount}("")` thay cho `transfer` để chống lỗi giới hạn 2.300 gas.

### 4.3. Đối chiếu với bản mẫu giảng viên và 4 điểm cốt lõi cần hiểu (Bước 3):
1. **Thứ tự Checks — Effects — Interactions:** Giúp ngăn chặn triệt để tấn công Reentrancy (sẽ thực hành khai thác lỗ hổng đảo ngược thứ tự này ở Lab 13).
2. **Custom Errors thay cho chuỗi revert dài:** Tiết kiệm khoảng 20-40% chi phí gas triển khai và hoàn trả gần như toàn bộ gas khi giao dịch bị hoàn tác sớm ở bước Checks.
3. **`call` thay cho `transfer`:** Khắc phục nhược điểm giới hạn 2.300 gas của `transfer`, tương thích tốt với tài khoản ví hợp đồng thông minh (Smart Contract Wallets / Account Abstraction).
4. **Từ khóa `indexed` trong sự kiện:** Đánh dấu địa chỉ `from` và `to` giúp DApp và Etherscan lập chỉ mục (index) tra cứu lịch sử nạp/rút tức thì.

### 4.4. Chuyển kỹ thuật vào sản phẩm nhóm (`ProjectCore.sol`):
- Nhóm đã khoanh vùng và tích hợp mô hình ký gửi có khóa thời gian vào cơ chế **Ký quỹ bảo đảm uy tín làng nghề (Reputation Staking with TimeLock)**:
  - Cơ sở sản xuất nộp cọc `0.05 ETH` qua `depositStake() payable`.
  - Tiền cọc bị khóa trong `stakeLockDuration` (30 ngày) và cơ sở chỉ được rút cọc qua `withdrawStake()` theo đúng thứ tự CEI sau khi hết thời hạn.
- **Kết quả biên dịch:** Hợp đồng `ProjectCore.sol` và `TimeLockVault.sol` biên dịch sạch 100% trên trình biên dịch Solidity `^0.8.20`.
