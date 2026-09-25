# NHẬT KÝ LÀM VIỆC VỚI AI — HỌC PHẦN ECO2432

---

## LAB 4 — NHẬN DIỆN HỢP ĐỒNG CÓ RỦI RO

### Lần 1 — Thẩm định rủi ro tệp hợp đồng `ClubTokens.sol`

**Prompt:**
```text
Bạn là chuyên viên thẩm định rủi ro tài sản số.
Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà
chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
– Tên hàm và số dòng
– Người nắm giữ token chịu rủi ro gì
Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ClubTokenA is ERC20 {
    constructor() ERC20("Club Token A", "CTA") {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }
}

contract ClubTokenB is ERC20, Ownable {
    constructor() ERC20("Club Token B", "CTB") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}

contract ClubTokenC is ERC20, Ownable {
    mapping(address => bool) public restricted;

    constructor() ERC20("Club Token C", "CTC") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }

    function setRestricted(address user, bool status) external onlyOwner {
        restricted[user] = status;
    }

    function _update(address from, address to, uint256 value) internal override {
        require(!restricted[from], "Dia chi bi han che");
        super._update(from, to, value);
    }
}
```

**AI trả về:**
AI chỉ ra Hợp đồng B có hàm `mint` (dòng 18–20) có nguy cơ lạm phát vô hạn. Ở Hợp đồng C, AI chỉ ra hàm `setRestricted` (dòng 30–32) có thể cấm người dùng giao dịch. Tuy nhiên, AI kết luận rằng Hợp đồng C cấm hoàn toàn mọi giao dịch nạp và rút của ví, đồng thời bỏ sót việc phân tích chi tiết dòng lệnh điều kiện `_update`.

**Đánh giá:** ⚠️ Phải sửa

---

### Bảng so sánh 3 khía cạnh bắt buộc theo yêu cầu Lab 4:

#### 1. Đọc thủ công tìm ra gì:
- **`ClubTokenA` (Dòng 7–11):** Không kế thừa `Ownable`, không có bất kỳ hàm quản trị hay biến owner nào. Tổng cung cố định 1,000,000 token ngay từ constructor, không thể mint thêm, an toàn tuyệt đối về mặt đặc quyền.
- **`ClubTokenB` (Dòng 13–21):** Có kế thừa `Ownable`, có hàm `mint` ở dòng 18–20 với modifier `onlyOwner` cho phép đúc token không giới hạn số lượng và không có trần tổng cung.
- **`ClubTokenC` (Dòng 23–38):** Có biến mapping `restricted` (dòng 24), hàm quản trị `setRestricted` (dòng 30–32) gắn `onlyOwner` và hàm ghi đè `_update` (dòng 34–37) có điều kiện `require(!restricted[from], "Dia chi bi han che");` tại dòng 35.

#### 2. AI tìm thêm được gì:
- AI giải thích rõ cơ chế OpenZeppelin v5: Hàm `_update` là hàm hook trung tâm điều phối mọi chuyển dịch token (thay thế cho `_beforeTokenTransfer` và `_afterTokenTransfer` ở phiên bản v4).
- AI mô tả chi tiết kịch bản lừa đảo trên thị trường thực tế: cơ chế của `ClubTokenB` thường bị kẻ xấu dùng để "xả hàng" (dumping token) sau khi gom thanh khoản; cơ chế của `ClubTokenC` là cấu trúc kinh điển của bẫy lừa đảo **Honeypot** trên các sàn giao dịch phi tập trung (DEX).

#### 3. AI có nói sai chỗ nào không (Lỗi do sinh viên phát hiện):
- **Sai sót 1 (Sai về logic kiểm tra điều kiện tại Hợp đồng C):**  
  AI kết luận: *"Hợp đồng C chặn cả việc chuyển và nhận token của địa chỉ bị đưa vào restricted"*.  
  $\rightarrow$ **Sinh viên phát hiện chỗ sai:** Khi soi kỹ dòng 35: `require(!restricted[from], "Dia chi bi han che");`, lệnh chỉ kiểm tra `restricted[from]`, tức là **chỉ chặn chiều gửi đi (from)**, hoàn toàn **không chặn chiều nhận vào (to)**. Điều này cực kỳ nguy hiểm vì nạn nhân vẫn nạp tiền hoặc mua token vào ví được bình thường nhưng khi muốn bán hoặc chuyển đi thì giao dịch bị revert — đúng 100% bản chất bẫy Honeypot.
- **Sai sót 2 (Bỏ sót số dòng làm bằng chứng quyết định):**  
  AI chỉ trích dẫn hàm `setRestricted` ở dòng 30–32 làm rủi ro chính mà không trích dẫn dòng 35 (`require(!restricted[from])`). Bản thân hàm `setRestricted` chỉ thay đổi một biến boolean trong mapping, chính dòng 35 trong hàm `_update` mới là vị trí trực tiếp tước đoạt quyền chuyển tiền của người nắm giữ.
- **Sai sót 3 (Ảo giác nhẹ về Hợp đồng A):**  
  AI ban đầu đưa ra khuyến cáo chung chung rằng *"Hợp đồng A có thể bị rủi ro nếu người tạo hợp đồng giữ toàn bộ token"*. Sinh viên đã đính chính: Yêu cầu đề bài là tìm **quyền đặc biệt mà chủ sở hữu có thể thực hiện qua các hàm**, mã nguồn của Hợp đồng A hoàn toàn không có hàm nào sau constructor, do đó Hợp đồng A không chứa quyền đặc biệt nào của admin.

---

**Cách sửa của sinh viên:**
1. Trích dẫn chính xác cặp số dòng bằng chứng cho Hợp đồng C: Dòng 30–32 (gán cấm) và Dòng 34–37 (đặc biệt Dòng 35 thực thi cấm chuyển đi).
2. Phân tích rõ cơ chế Honeypot một chiều của Hợp đồng C (chặn `from`, không chặn `to`).
3. Hoàn thiện bảng đối chiếu 3 hợp đồng trong [Lab 1-7/lab04.md](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/lab04.md).

**Ai phát hiện:** **Sinh viên phát hiện**