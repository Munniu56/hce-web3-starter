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

---

## LAB 6 — SINH MÃ BẰNG AI VÀ KIỂM TRA KẾT QUẢ

**Tệp mã nguồn:** [`Lab 1-7/analyze_wallet.py`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/analyze_wallet.py)  
**Tác giả:** Ngô Thị Thuý Vân — **Mã SV:** 23K4300023 — **Lớp:** K57 - Kinh tế số  
**Địa chỉ ví kiểm thử:** `0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01`  
**Tuân thủ đặc tả:** [`SPEC.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/SPEC.md) và quy ước [`AGENTS.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/AGENTS.md)  
**Chuẩn đầu ra Lab 6:** Chương trình chạy ra được biểu đồ, và sinh viên ghi nhận được tối thiểu 2 lỗi do công cụ AI sinh ra.

---

### Bảng đối chiếu 6 điểm kiểm tra bắt buộc (Trang 15 Sổ tay thực hành ECO2432)

| # | Hạng mục kiểm tra | Cách kiểm tra trong mã nguồn | Đánh giá đạt chuẩn | Lỗi hay gặp của AI & Cách sinh viên xử lý |
| :-: | :--- | :--- | :-: | :--- |
| **1** | **Đơn vị tiền tệ** | Kiểm tra việc chia $10^{18}$ trước khi tính toán và hiển thị |  ĐẠT | AI thường quên chia $10^{18}$ cho phí gas hoặc hiển thị số nguyên 19 chữ số. Sinh viên định nghĩa hằng số `WEI_PER_ETH = 10**18` và quy đổi ngay khi bóc tách JSON (dòng 45, 227–228). |
| **2** | **Bảo mật khóa API** | Tìm chuỗi khóa API trong mã nguồn |  ĐẠT | AI thường viết `API_KEY = "YOUR_KEY_HERE"`. Sinh viên triệt để tuân thủ quy tắc 1 trong `AGENTS.md`: đọc từ `os.environ.get("ETHERSCAN_API_KEY")` (dòng 71–83). |
| **3** | **Phân trang tự động** | Kiểm tra vòng lặp lấy dữ liệu khi ví $> 10,000$ giao dịch |  ĐẠT | AI chỉ gọi một request đơn lẻ. Sinh viên thiết kế vòng lặp `while page <= MAX_PAGES` với `offset = PAGE_SIZE`, kiểm tra điều kiện dừng và thêm `time.sleep(0.22)` chống Rate Limit (dòng 150–196). |
| **4** | **Giao dịch thất bại** | Kiểm tra hạch toán phí gas khi `isError == "1"` |  ĐẠT | AI mặc định dùng `continue` bỏ qua toàn bộ. Sinh viên bắt lỗi và tách nhánh trừ phí gas thực tế khỏi số dư ví (dòng 278–289). |
| **5** | **Xử lý lỗi hệ thống** | Thử khóa API sai, địa chỉ sai, lỗi kết nối mạng |  ĐẠT | Kiểm tra định dạng ví EIP-55 (E4, dòng 54–66), bóc tách mã lỗi Etherscan `NOTOK`, `Invalid API Key`, và nhận diện `No transactions found` là trạng thái rỗng hợp lệ E1 (dòng 88–125). |
| **6** | **Phiên bản API hiện hành** | Đối chiếu endpoint với tài liệu Etherscan 2026 |  ĐẠT | AI sinh mã dùng endpoint v1 cũ. Sinh viên đối chiếu tài liệu và nâng cấp lên Etherscan API v2 với `chainid=1` (dòng 44, 48, 94). |

---

### Lần 1 — Lỗi Endpoint Etherscan API cũ và thiếu tham số `chainid` (Điểm kiểm tra 6)

**Prompt:**
```text
Đọc tệp SPEC.md trong dự án và viết chương trình Python thực hiện đúng đặc tả đó.
Tuân thủ các quy ước trong AGENTS.md.
Trước khi viết mã, tóm tắt lại cách bạn hiểu yêu cầu để tôi xác nhận.
Viết hàm gọi API Etherscan để lấy danh sách giao dịch ETH của ví trong 90 ngày.
```

**AI trả về:**
AI sinh hàm gọi Etherscan API sử dụng endpoint v1 truyền thống:
```python
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={api_key}"
```

**Đánh giá:** ⚠️ Phải sửa

**Chỗ sai:**
- **Vị trí:** Trong cấu hình URL gốc của API.
- **Mô tả kỹ thuật:** Etherscan đã chuyển đổi toàn bộ hạ tầng sang cổng **API v2 hợp nhất** (`https://api.etherscan.io/v2/api`). Khi gọi endpoint v2, tham số `chainid` là **bắt buộc** (`chainid=1` cho Ethereum Mainnet, `chainid=11155111` cho Sepolia Testnet). Endpoint v1 cũ bị giới hạn hoặc trả về cảnh báo phản hồi lỗi `NOTOK`. Do dữ liệu huấn luyện của AI chỉ dừng ở các năm trước, AI mặc định sử dụng endpoint cũ `api.etherscan.io/api`.
- **Dữ liệu đối chiếu:** Etherscan Developer Documentation (2026 Release) — Unified Multi-chain API v2.

**Cách sửa của sinh viên:**
1. Định nghĩa hằng số URL chuẩn Etherscan API v2: `ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"` (dòng 44).
2. Định nghĩa hằng số mạng `CHAIN_ID = 1` (Mainnet) hoặc `11155111` (Sepolia) (dòng 48).
3. Trong hàm `etherscan_get()`, tự động chèn hai tham số bắt buộc vào mọi request:
   ```python
   params["chainid"] = CHAIN_ID
   params["apikey"] = api_key
   ```
   (dòng 94–95 trong [`analyze_wallet.py`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/analyze_wallet.py#L94-L95)).

**Ai phát hiện:** **Sinh viên phát hiện** (sau khi đối chiếu với tài liệu chính thức Etherscan).

---

### Lần 2 — Lỗi bỏ sót phí gas của giao dịch gửi đi thất bại (Quy tắc R4 & Điểm kiểm tra 4)

**Prompt:**
```text
Viết hàm process_transactions(txs, address) phân loại dòng tiền vào và ra theo các quy tắc R1, R2, R3, R4 trong SPEC.md.
```

**AI trả về:**
AI xử lý điều kiện giao dịch thất bại bằng cách bỏ qua toàn bộ:
```python
for tx in txs:
    if tx.get("isError") == "1":
        continue  # Giao dịch thất bại thì bỏ qua, không tính biến động
```

**Đánh giá:** ❌ Sai, bỏ

**Chỗ sai:**
- **Vị trí:** Đoạn kiểm tra trạng thái `isError` trong vòng lặp giao dịch.
- **Mô tả kỹ thuật:** Đây là lỗ hổng nghiêm trọng về hiểu biết cơ chế máy ảo Ethereum (EVM). Khi một giao dịch do chính ví gửi đi (`from == address`) bị lỗi (ví dụ: `reverted`, `out of gas`, hoặc sai tham số hợp đồng): EVM sẽ hoàn lại số tiền chuyển (`value`), **nhưng toàn bộ phí gas (`gasUsed * gasPrice`) vẫn bị trừ vĩnh viễn khỏi số dư ví**! Nếu AI dùng `continue` bỏ qua toàn bộ, số dư tích lũy của ví trên báo cáo sẽ cao hơn số dư thực tế trên blockchain, làm sai lệch báo cáo kế toán tài sản số.
- **Dữ liệu đối chiếu:** Quy tắc R4 trong `SPEC.md`: *"Giao dịch có trạng thái thất bại vẫn bị trừ phí, phải tính vào dòng tiền ra"*.

**Cách sửa của sinh viên:**
Tái cấu trúc lại luồng rẽ nhánh điều kiện trong `process_transactions()` (dòng 264–289):
```python
elif is_from_me:
    if is_error == "0":
        # R3: Giao dịch thành công — trừ cả value và phí gas
        balance -= (value_eth + fee_eth)
        records.append({
            "flow_type": "RA",
            "amount_eth": value_eth,
            "fee_eth": fee_eth,
            "balance_eth": balance,
            "note": "outflow-ok"
        })
    else:
        # R4: Giao dịch thất bại — EVM hoàn lại value, NHƯNG phí gas vẫn bị trừ
        balance -= fee_eth
        records.append({
            "flow_type": "RA",
            "amount_eth": 0.0,  # Value được hoàn lại, không tính vào dòng tiền ra
            "fee_eth": fee_eth,
            "balance_eth": balance,
            "note": "outflow-failed"
        })
```

**Ai phát hiện:** **Sinh viên phát hiện**.

---

### Lần 3 — Lỗi số dư đầu kỳ gán bằng 0 dẫn đến số dư âm trên biểu đồ (Quy tắc R8 & Điểm kiểm tra 1)

**Prompt:**
```text
Tính số dư lũy kế qua từng giao dịch và vẽ biểu đồ đường biểu diễn số dư theo thời gian trong 90 ngày gần nhất.
```

**AI trả về:**
AI khởi tạo số dư bắt đầu từ 0:
```python
balance = 0.0
for tx in txs:
    # cộng trừ biến động vào balance...
```

**Đánh giá:** ⚠️ Phải sửa

**Chỗ sai:**
- **Vị trí:** Khởi tạo biến `balance = 0.0` ở đầu hàm tính toán.
- **Mô tả kỹ thuật:** Nếu ví đã có sẵn tài sản tích lũy từ trước kỳ 90 ngày (ví dụ: đang có $10\text{ ETH}$), và giao dịch đầu tiên phát sinh trong kỳ 90 ngày là một lệnh chuyển đi $4\text{ ETH}$: Việc gán số dư đầu kỳ bằng `0` sẽ khiến số dư lũy kế tức thời bị rơi xuống $-4\text{ ETH}$. Trên blockchain Ethereum, tài khoản không thể có số dư âm. Biểu đồ đường vẽ ra sẽ bị âm dưới trục hoành, vi phạm nguyên tắc cơ bản của kế toán.
- **Dữ liệu đối chiếu:** Quy tắc bổ sung R8 trong `SPEC.md` do nhóm hoàn thiện ở Lab 5.

**Cách sửa của sinh viên:**
Xây dựng thuật toán suy diễn số dư đầu kỳ thực tế (R8) tại hàm `main()` (dòng 484–495):
1. Gọi API `account.balance` (`fetch_balance`) để lấy số dư hiện tại trên chuỗi ($B_{\text{hiện tại}}$).
2. Chạy thử `process_transactions` với số dư ban đầu bằng `0.0` để tính tổng dòng tiền ròng phát sinh trong 90 ngày:
   $$\text{Net Flow} = \sum \text{Inflow} - \sum \text{Outflow}$$
3. Suy ngược số dư chính xác tại mốc bắt đầu kỳ phân tích:
   $$\text{Initial Balance} = B_{\text{hiện tại}} - \text{Net Flow}$$
4. Sau đó mới chạy hàm `process_transactions()` chính thức với `initial_balance` này để số dư luôn dương và trùng khớp 100% với số dư sổ cái on-chain.

**Ai phát hiện:** **Sinh viên phát hiện**.

---

### Lần 4 — Lỗi mã hóa ký tự Unicode Box-Drawing gây sập console Windows PowerShell

**Prompt:**
```text
Viết hàm print_summary(df, current_balance) để in 3 chỉ số kinh tế tổng hợp đẹp mắt với khung viền ngăn cách.
```

**AI trả về:**
AI sử dụng ký tự vẽ khung Unicode:
```python
print("\n" + "─" * 54)
print("  CHI SO TONG HOP (SUMMARY METRICS)")
print("─" * 54)
```

**Đánh giá:** ⚠️ Phải sửa

**Chỗ sai:**
- **Vị trí:** Dòng in ký tự `"─"` (Unicode `\u2500` - Box Drawings Light Horizontal).
- **Mô tả kỹ thuật:** Trên hệ điều hành Windows, PowerShell và CMD mặc định sử dụng bảng mã ANSI/OEM địa phương (như `cp1252` hoặc `cp437`). Khi gọi `print("─")`, bộ giải mã `charmap` không thể ánh xạ ký tự Unicode này, dẫn đến văng lỗi nghiêm trọng:
  ```text
  UnicodeEncodeError: 'charmap' codec can't encode characters in position 2-55: character maps to <undefined>
  ```
  Chương trình bị sập ngay tại bước hiển thị kết quả cuối cùng dù các bước xử lý dữ liệu trước đó đều thành công.

**Cách sửa của sinh viên:**
1. Thêm đoạn mã cấu hình ép kiểu `sys.stdout` và `sys.stderr` sang `utf-8` ở đầu chương trình (dòng 29–35):
   ```python
   if hasattr(sys.stdout, "reconfigure"):
       try:
           sys.stdout.reconfigure(encoding="utf-8")
           sys.stderr.reconfigure(encoding="utf-8")
       except Exception:
           pass
   ```
2. Thay thế ký tự Unicode `"─"` bằng ký tự gạch ngang ASCII tiêu chuẩn `"-" * 54` tại hàm `print_summary()` (dòng 434–445).

**Ai phát hiện:** **Sinh viên phát hiện** khi chạy thực nghiệm trong môi trường Windows PowerShell.

---

### Lần 5 — Lỗi xử lý giao dịch tự chuyển cho chính mình (Self-Transfer - Quy tắc R7)

**Prompt:**
```text
Phân loại dòng tiền: nếu to == address thì là dòng tiền vào, nếu from == address thì là dòng tiền ra.
```

**AI trả về:**
AI viết hai khối lệnh `if` độc lập:
```python
if tx["to"] == address:
    balance += value
if tx["from"] == address:
    balance -= (value + fee)
```

**Đánh giá:** ⚠️ Phải sửa

**Chỗ sai:**
- Khi người dùng gửi giao dịch tự chuyển ETH sang chính ví của mình (`from == to`), AI cộng giá trị `value` vào Inflow và đồng thời trừ `value + fee` ở Outflow $\rightarrow$ làm doanh số dòng tiền bị thổi phồng gấp đôi, trong khi thực tế số dư ròng của ví chỉ suy giảm một khoản bằng đúng tiền phí gas.

**Cách sửa của sinh viên:**
Bổ sung nhánh kiểm tra ưu tiên `is_from_me and is_to_me` (quy tắc R7, dòng 234–246 trong `analyze_wallet.py`):
```python
if is_from_me and is_to_me:
    balance -= fee_eth
    records.append({
        "flow_type": "RA",
        "amount_eth": 0.0,      # Value không làm biến động số dư ròng
        "fee_eth": fee_eth,
        "balance_eth": balance,
        "note": "self-transfer",
    })
    continue
```

**Ai phát hiện:** **Sinh viên phát hiện**.

---

### Kết quả kiểm chứng thực nghiệm & Sản phẩm nộp Lab 6

1. **Chương trình thực thi hoàn chỉnh:**
   - Script [`Lab 1-7/analyze_wallet.py`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/analyze_wallet.py) chạy mượt mà, vượt qua toàn bộ 6/6 tiêu chí kiểm tra bắt buộc.
2. **Bảng đối soát giao dịch và 3 chỉ số kinh tế tổng hợp:**
   ```text
   ============================================================================================================
   Thoi gian (UTC)        Tx Hash            Loai      So tien (ETH)  Phi gas (ETH)   So du luy ke (ETH) Ghi chu
   ============================================================================================================
   2026-01-22 16:40:00    0xfa1234...90abcd  VAO          5.00000000     0.00000000           5.50000000 inflow
   2026-01-24 01:57:36    0x199e95...cf98a3  RA           4.00000000     0.00005393           1.49994607 outflow-ok
   2026-01-25 00:13:20    0xbb1234...90bbbb  RA           0.00000000     0.00004200           1.49990407 outflow-failed
   2026-01-26 04:00:00    0xcc1234...90cccc  RA           0.00000000     0.00004200           1.49986207 self-transfer
   2026-01-27 07:46:40    0xdd1234...90dddd  VAO          1.50000000     0.00000000           2.99986207 inflow
   ============================================================================================================
   Tong so giao dich hien thi: 5

   ------------------------------------------------------
     CHI SO TONG HOP (SUMMARY METRICS)
   ------------------------------------------------------
     Tong tien vao (Total Inflow)  :       6.50000000 ETH
     Tong tien ra  (Total Outflow) :       4.00013793 ETH
     So du cuoi ky (Closing Bal.)  :       2.99986207 ETH
     Bien dong rong (Net Flow)     :      +2.49986207 ETH
   ------------------------------------------------------
   ```
3. **Biểu đồ số dư lũy kế trực quan:**
   - Đã xuất và lưu tệp hình ảnh tại: [`Lab 1-7/balance_chart_0x5856b2.png`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/balance_chart_0x5856b2.png)
   - Thể hiện trực quan đường số dư lũy kế luôn dương, phân biệt rõ điểm giao dịch nạp vào (màu xanh lá) và rút ra/trả phí gas (màu đỏ).