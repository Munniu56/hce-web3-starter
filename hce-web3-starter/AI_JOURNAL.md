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
**Địa chỉ ví cá nhân kiểm thử:** `0x82d022a704706B2f144863D619D7418F8a0f19A7` (Mạng Sepolia Testnet, Chain ID: `11155111`)  
**Địa chỉ ví kiểm thử Mainnet:** `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (vitalik.eth, Chain ID: `1`)  
**Tuân thủ đặc tả:** [`SPEC.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/SPEC.md) và quy ước [`AGENTS.md`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/AGENTS.md)  
**Chuẩn đầu ra Lab 6:** Chương trình chạy ra được biểu đồ, và sinh viên ghi nhận được tối thiểu 2 lỗi do công cụ AI sinh ra.

---

### Bảng đối chiếu 6 điểm kiểm tra bắt buộc (Trang 15 Sổ tay thực hành ECO2432)

| # | Hạng mục kiểm tra | Cách kiểm tra trong mã nguồn | Đánh giá đạt chuẩn | Lỗi hay gặp của AI & Cách sinh viên xử lý |
| :-: | :--- | :--- | :-: | :--- |
| **1** | **Đơn vị tiền tệ** | Kiểm tra việc chia $10^{18}$ trước khi tính toán và hiển thị | ĐẠT | AI thường quên chia $10^{18}$ cho phí gas hoặc hiển thị số nguyên 19 chữ số. Sinh viên định nghĩa hằng số `WEI_PER_ETH = 10**18` và quy đổi ngay khi bóc tách JSON (dòng 45, 234–236). |
| **2** | **Bảo mật khóa API** | Tìm chuỗi khóa API trong mã nguồn | ĐẠT | AI thường viết `API_KEY = "NJ6J6R76..."`. Sinh viên triệt để tuân thủ quy tắc 1 trong `AGENTS.md`: đọc từ `os.environ.get("ETHERSCAN_API_KEY")` (dòng 79–90), tuyệt đối không hardcode khóa API. |
| **3** | **Phân trang tự động** | Kiểm tra vòng lặp lấy dữ liệu khi ví $> 10,000$ giao dịch | ĐẠT | AI chỉ gọi một request đơn lẻ hoặc dùng `sort="asc"` từ block 0 khiến kẹt dữ liệu cũ. Sinh viên dùng vòng lặp phân trang tự động kết hợp `sort="desc"` lấy từ giao dịch mới nhất trong kỳ 90 ngày (dòng 158–203). |
| **4** | **Giao dịch thất bại** | Kiểm tra hạch toán phí gas khi `isError == "1"` | ĐẠT | AI mặc định dùng `continue` bỏ qua toàn bộ. Sinh viên bắt lỗi và tách nhánh trừ phí gas thực tế khỏi số dư ví theo quy tắc R4 (dòng 285–296). |
| **5** | **Xử lý lỗi hệ thống** | Thử khóa API sai, địa chỉ sai, lỗi kết nối mạng | ĐẠT | Kiểm tra định dạng ví EIP-55 (E4, dòng 62–73), bóc tách mã lỗi Etherscan `NOTOK`, `Invalid API Key`, và nhận diện `No transactions found` là trạng thái rỗng hợp lệ E1 (dòng 96–133). |
| **6** | **Phiên bản API hiện hành** | Đối chiếu endpoint với tài liệu Etherscan 2026 | ĐẠT | AI sinh mã dùng endpoint v1 cũ. Sinh viên đối chiếu tài liệu và nâng cấp lên Etherscan API v2 với `chainid` hỗ trợ đa mạng (dòng 52, 98, 102). |

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
1. Định nghĩa hằng số URL chuẩn Etherscan API v2: `ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"`.
2. Hỗ trợ tham số dòng lệnh `--chainid` (mặc định 1 cho Mainnet, hỗ trợ 11155111 cho Sepolia).
3. Trong hàm `etherscan_get()`, tự động chèn hai tham số bắt buộc vào mọi request:
   ```python
   params["chainid"] = chain_id
   params["apikey"] = api_key
   ```

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
Tái cấu trúc lại luồng rẽ nhánh điều kiện trong `process_transactions()`:
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
Xây dựng thuật toán suy diễn số dư đầu kỳ thực tế (R8) tại hàm `main()`:
1. Gọi API `account.balance` (`fetch_balance`) để lấy số dư hiện tại trên chuỗi ($B_{\text{hiện tại}}$).
2. Chạy thử `process_transactions` với số dư ban đầu bằng `0.0` để tính tổng dòng tiền ròng phát sinh trong 90 ngày:
   $$\text{Net Flow} = \sum \text{Inflow} - \sum \text{Outflow}$$
3. Suy ngược số dư chính xác tại mốc bắt đầu kỳ phân tích:
   $$\text{Initial Balance} = B_{\text{hiện tại}} - \text{Net Flow}$$
4. Sau đó mới chạy hàm `process_transactions()` chính thức với `initial_balance` này để số dư luôn dương và trùng khớp 100% với số dư sổ cái on-chain.

**Ai phát hiện:** **Sinh viên phát hiện**.

---

### Lần 4 — Lỗi phân trang `sort="asc"` từ block 0 làm mất trắng giao dịch trong kỳ 90 ngày (Điểm kiểm tra 3)

**Prompt:**
```text
Viết hàm fetch_transactions để tải danh sách giao dịch có phân trang khi số lượng giao dịch vượt quá 10,000 bản ghi.
```

**AI trả về:**
AI gọi Etherscan API với `sort="asc"` và lọc dữ liệu client-side:
```python
params = {
    "module": "account", "action": "txlist", "address": address,
    "page": page, "offset": 10000, "sort": "asc"
}
data = etherscan_get(params)
filtered = [tx for tx in data["result"] if start_ts <= int(tx["timeStamp"]) <= end_ts]
if len(data["result"]) < 10000:
    break
```

**Đánh giá:** ❌ Sai, bỏ

**Chỗ sai:**
- **Mô tả kỹ thuật:** Đây là lỗi tư duy nghiêm trọng của AI khi xử lý dữ liệu chuỗi thời gian lớn. Khi thiết lập `sort="asc"`, API sẽ trả về các giao dịch cổ nhất từ lúc ví mới tạo (năm 2015-2016). Trang 1 chỉ chứa các giao dịch cách đây 8-10 năm, hoàn toàn không có giao dịch nào trong 90 ngày gần nhất (`filtered == []`). Hơn nữa, nếu tổng số giao dịch cổ nhỏ hơn 10,000, câu lệnh `if len(data["result"]) < 10000: break` sẽ kích hoạt dừng ngay lập tức, khiến chương trình báo rỗng `"Vi khong co giao dich trong ky"` dù ví hoạt động rất sôi động trong 90 ngày qua!

**Cách sửa của sinh viên:**
Thay đổi cơ chế lấy dữ liệu sang `sort="desc"` để quét từ các giao dịch mới nhất ngược về quá khứ:
```python
params["sort"] = "desc"
# Lấy giao dịch mới nhất trước, nếu gặp giao dịch có timestamp < start_ts thì dừng lấy tiếp
for tx in result:
    tx_ts = int(tx["timeStamp"])
    if tx_ts < start_ts:
        reached_before_start = True
        break
    elif tx_ts <= end_ts:
        collected_txs.append(tx)
# Sau đó đảo ngược hoặc sắp xếp lại tăng dần theo thời gian (R6) trước khi tính toán
collected_txs.sort(key=lambda x: int(x["timeStamp"]))
```

**Ai phát hiện:** **Sinh viên phát hiện** khi chạy thử nghiệm trên các ví Ethereum lâu năm.

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
Bổ sung nhánh kiểm tra ưu tiên `is_from_me and is_to_me` (quy tắc R7):
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

### Lần 6 — Lỗi mã hóa ký tự Unicode Box-Drawing gây sập console Windows PowerShell

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
- Trên Windows, PowerShell và CMD mặc định sử dụng bảng mã ANSI/OEM địa phương (`cp1252`/`cp437`). Ký tự Unicode `"─"` gây văng lỗi `UnicodeEncodeError: 'charmap' codec can't encode character`, làm sập chương trình.

**Cách sửa của sinh viên:**
1. Thêm cấu hình ép kiểu `sys.stdout` và `sys.stderr` sang `utf-8` ở đầu script.
2. Thay thế ký tự Unicode `"─"` bằng ký tự gạch ngang ASCII chuẩn `"-" * 54`.

**Ai phát hiện:** **Sinh viên phát hiện** khi chạy thực nghiệm trong môi trường Windows PowerShell.

---

### Kết quả kiểm chứng thực nghiệm & Sản phẩm nộp Lab 6

1. **Chương trình thực thi hoàn chỉnh:**
   - Script [`Lab 1-7/analyze_wallet.py`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/analyze_wallet.py) chạy mượt mà, vượt qua toàn bộ 6/6 tiêu chí kiểm tra bắt buộc.
2. **Bằng chứng chạy thực tế với khóa API trên ví sinh viên (`0x82d022a704706B2f144863D619D7418F8a0f19A7` - Sepolia Testnet, Chain ID 11155111):**
   ```text
   ======================================================
     Phan tich vi  : 0x82d022a704706b2f144863d619d7418f8a0f19a7
     Mang luoi     : Chain ID 11155111
     Khoang thoi gian: 90 ngay (2026-06-29 -> hom nay)
   ======================================================

   [1/3] Lay so du hien tai cua vi...
     So du hien tai: 7.48916329 ETH

   [2/3] Tai danh sach giao dich...
     Dang tai giao dich (10000 ban ghi/trang, toi da 100 trang)...
       Trang 1: 36 ban ghi lay ve, trong ky: 5
     Tong giao dich trong ky da loc (R6): 5

   [3/3] Xu ly giao dich va tinh toan...
     Dong tien rong trong ky (R8): +1.09594778 ETH
     So du dau ky tinh duoc  (R8): 6.39321550 ETH

   ============================================================================================================
   Thoi gian (UTC)        Tx Hash            Loai      So tien (ETH)  Phi gas (ETH)   So du luy ke (ETH) Ghi chu
   ============================================================================================================
   2026-09-08 07:49:12    0xa6c941...ab9e0b  VAO          1.15100000     0.00000000           7.54421550 inflow
   2026-09-10 06:54:24    0xf1b9c7...c1131d  RA           2.00000000     0.00005222           5.54416329 outflow-ok
   2026-09-10 07:03:36    0x9558eb...c88be7  VAO          0.11000000     0.00000000           5.65416329 inflow
   2026-09-10 07:16:12    0x9277e9...948821  VAO          0.10000000     0.00000000           5.75416329 inflow
   2026-09-10 07:48:00    0xffa9fc...bbb06f  VAO          1.73500000     0.00000000           7.48916329 inflow
   ============================================================================================================
   Tong so giao dich hien thi: 5

   ------------------------------------------------------
     CHI SO TONG HOP (SUMMARY METRICS)
   ------------------------------------------------------
     Tong tien vao (Total Inflow)  :       3.09600000 ETH
     Tong tien ra  (Total Outflow) :       2.00005222 ETH
     So du cuoi ky (Closing Bal.)  :       7.48916329 ETH
     Bien dong rong (Net Flow)     :      +1.09594778 ETH
   ------------------------------------------------------
   ```
3. **Biểu đồ số dư lũy kế trực quan:**
   - Đã xuất và lưu tệp hình ảnh tại: [`Lab 1-7/bieu_do_so_du_lab06.png`](file:///d:/Antigravity%20IDE/hce-web3-starter/hce-web3-starter/Lab%201-7/bieu_do_so_du_lab06.png).
   - Biểu đồ thể hiện chính xác đường số dư lũy kế luôn dương, phân biệt rõ điểm giao dịch nạp vào (màu xanh lá) và chuyển đi (màu đỏ).