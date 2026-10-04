# HueLegend — Hệ Thống Truy Xuất Nguồn Gốc Đặc Sản Huế Trên Blockchain

Dự án nghiên cứu & ứng dụng hợp đồng thông minh thuộc học phần **ECO2432 - Tiền điện tử và Hợp đồng thông minh**.

---

## 📌 1. Giới thiệu sản phẩm & Bài toán giải quyết

**HueLegend** là nền tảng Web3 DApp chuyên biệt hóa cho việc bảo hộ và truy xuất nguồn gốc chuỗi cung ứng các đặc sản truyền thống xứ Huế (Mè xửng, Tôm chua, Trà Cung đình, Tinh dầu tràm, Nón bài thơ,...).

### 🔍 Bài toán thực tiễn:
- **Cơ sở sản xuất & Làng nghề:** Cần công cụ minh bạch, bất biến trên Blockchain để chứng minh nguồn gốc xuất xứ nguyên liệu sạch đạt chuẩn OCOP, bảo vệ danh tiếng thương hiệu trước tình trạng hàng giả mạo, nhái nhãn mác tràn lan tại các điểm du lịch.
- **Đơn vị Vận chuyển & Điểm bán lẻ:** Cần cơ chế xác nhận trách nhiệm qua chữ ký mật mã (ví Web3), lưu lại hành trình vận chuyển, điều kiện lưu kho để tránh rủi ro đền bù sai lệch.
- **Khách mua hàng & Du khách:** Cần một phương thức nhanh chóng: chỉ cần dùng camera điện thoại quét mã QR dán trên bao bì là có thể xem toàn bộ dòng thời gian (timeline) bất biến từ lúc gieo trồng/thu hoạch đến khi lên kệ, hoàn toàn không thể bị làm giả hay tẩy xóa.

---

## 🚀 2. Luồng cốt lõi Demo (Core Workflow)

```
[1. Tạo lô đặc sản]           [2. Thêm chặng bởi đúng vai]           [3. Quét QR xem lịch sử]
  (Cơ sở sản xuất)         (Vận chuyển / Kiểm định / Điểm bán)         (Khách mua hàng)
         │                                   │                                │
         ▼                                   ▼                                ▼
- Nhập thông tin lô hàng            - Kiểm tra quyền ví on-chain       - Quét camera mã QR
- Ký giao dịch khởi tạo             - Xác thực đúng vai trò hợp lệ     - Xem timeline từng chặng
- Tự động sinh mã QR động           - Ngăn chặn mạo danh (Revert)      - Đối soát TxHash Sepolia
```

1. **Tạo lô (Create Batch):** Cơ sở sản xuất (`ROLE_PRODUCER`) đưa thông tin lô hàng lên hợp đồng `ProjectCore.sol` kèm vùng nguyên liệu và mã định danh. Hệ thống tự sinh mã QR Code.
2. **Thêm chặng bởi đúng vai (Role-based Checkpoint):** Đơn vị vận chuyển (`ROLE_LOGISTICS`), cơ quan kiểm định (`ROLE_INSPECTOR`) hay cửa hàng bán lẻ (`ROLE_RETAILER`) tiếp nhận hàng và ký giao dịch ghi nhận chặng. Hệ thống tự động từ chối (`revert UnauthorizedCaller`) nếu địa chỉ ví chưa được cấp quyền tương ứng (phòng chống gian lận).
3. **Quét QR xem lịch sử (Scan & Trace):** Người tiêu dùng quét mã QR để tra cứu trực tiếp toàn bộ các chặng trên blockchain miễn phí gas.

---

## 📂 3. Cấu trúc thư mục dự án (Chuẩn Lab 8)

```text
HueLegend/
├── README.md               # Giới thiệu sản phẩm, bài toán và hướng dẫn chạy
├── AGENTS.md               # Quy ước kỹ thuật và nguyên tắc sinh mã cho AI
├── docs/
│   ├── PROJECT_PLAN.md     # Kế hoạch dự án, phân công vai trò và mốc công việc
│   ├── SPEC.md             # Đặc tả yêu cầu kỹ thuật và quy tắc nghiệp vụ
│   ├── AI_JOURNAL.md       # Nhật ký làm việc cùng AI và các lỗi bảo mật phát hiện
│   ├── ECONOMIC_RULES.md   # Quy tắc kinh tế, ký quỹ uy tín và cơ chế phạt gian lận
│   └── PRESENTATION_PLAN.md# Kịch bản demo và phân công thuyết trình bảo vệ
├── contracts/
│   ├── training/           # Bài mẫu học kỹ thuật (ClassPoint, TimeLockVault...)
│   └── project/
│       └── ProjectCore.sol # Hợp đồng thông minh cốt lõi của HueLegend
├── test/
│   └── ProjectCore.test.js # Bộ kiểm thử tự động (bao gồm ca gian lận TC-03)
├── web/
│   └── index.html          # Giao diện Web3 DApp sản phẩm (Huế Royal Theme)
└── evidence/
    └── lab-08...lab-15/    # Biên bản, ảnh chụp màn hình và TxHash từng lab
```

---

## ⚙️ 4. Hướng dẫn cài đặt & Chạy sản phẩm

### 4.1. Mở giao diện Web DApp:
- Mở trực tiếp tệp [`web/index.html`](./web/index.html) bằng trình duyệt web (Google Chrome, MS Edge, Brave).
- Hoặc sử dụng Live Server / VS Code / Antigravity Webview.
- Giao diện tích hợp sẵn **Interactive Demo Engine** với dữ liệu mẫu các đặc sản Huế và bộ tạo mã QR động chạy ngay lập tức.

### 4.2. Biên dịch & Triển khai Smart Contract qua Remix IDE:
1. Mở [Remix IDE](https://remix.ethereum.org).
2. Tải tệp [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) lên Remix.
3. Chọn trình biên dịch Solidity phiên bản `0.8.20` hoặc `0.8.24`.
4. Triển khai hợp đồng lên môi trường **Injected Provider - MetaMask** (Mạng Ethereum Sepolia Testnet).

### 4.3. Chạy kiểm thử tự động:
```bash
npx hardhat test test/ProjectCore.test.js
```

---

## 🌐 5. Thông tin triển khai & Đường dẫn chạy thật

- **Mạng Blockchain:** Ethereum Sepolia Testnet
- **Địa chỉ ví Admin / Triển khai:** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Địa chỉ Hợp đồng thông minh:** *(Cập nhật sau khi deploy Sepolia ở Lab 11)*
- **Liên kết Demo Web DApp:** [Mở DApp cục bộ tại `web/index.html`](./web/index.html)
- **Mẫu commit chuẩn:** `lab-08: [khoi tao cau truc du an HueLegend]`
