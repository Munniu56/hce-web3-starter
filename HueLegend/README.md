# HueLegend — Hệ Thống Truy Xuất Nguồn Gốc Đặc Sản Huế Trên Blockchain

> **Câu giới thiệu sản phẩm (Checkpoint 1):**  
> *"Nhóm xây HueLegend cho các cơ sở làng nghề và du khách mua đặc sản Huế để minh bạch lịch sử nguồn gốc từng lô hàng qua mã QR bất biến trên blockchain."*

---

## 🧭 BỐN CÂU HỎI ĐẦU RA THEO CHUẨN LAB 8

| Câu hỏi | Câu trả lời của dự án HueLegend |
| :--- | :--- |
| **1. Nhóm làm gì?** | Xây dựng hệ thống Web3 DApp và Smart Contract trên Ethereum Sepolia để ghi nhận, xác thực và truy xuất lịch sử chuỗi cung ứng bất biến cho các đặc sản truyền thống xứ Huế (Mè xửng, Tôm chua, Trà Cung đình, Tinh dầu tràm, Nón bài thơ). |
| **2. Làm cho ai?** | - **Cơ sở sản xuất & Hợp tác xã làng nghề:** Minh bạch nguồn gốc, bảo vệ thương hiệu độc quyền.<br>- **Đơn vị vận chuyển & Điểm bán lẻ:** Xác nhận trách nhiệm bàn giao rõ ràng.<br>- **Du khách & Người tiêu dùng:** Quét mã QR kiểm chứng hàng thật, an tâm về chất lượng. |
| **3. Quy tắc chính là gì?** | 1. **Khởi tạo lô:** Chỉ cơ sở có `ROLE_PRODUCER` mới được tạo mã lô duy nhất kèm thông tin xưởng.<br>2. **Thêm chặng theo vai:** Phải có đúng vai trò (`ROLE_LOGISTICS`, `ROLE_RETAILER`,...) mới được ký giao dịch ghi nhận chặng.<br>3. **Chống gian lận:** Mạo danh bị revert ngay lập tức (`UnauthorizedCaller`); cơ sở gian lận bị tịch thu cọc 0.05 ETH trích thưởng 50% cho người tố giác.<br>4. **Tra cứu tự do:** Người mua quét QR xem dòng thời gian (timeline) hoàn toàn miễn phí gas. |
| **4. Mỗi thành viên chịu trách nhiệm phần nào?** | - **Ngô Thị Thuỷ Vân:** Vai chính Lab 8–11: Hợp đồng (Smart Contract) \| Vai chính Lab 12–15: Kiểm thử (QA & Audit).<br>- **Lê Thị Thảo Nhi:** Vai chính Lab 8–11: Đặc tả (SPEC & BA) \| Vai chính Lab 12–15: Giao diện (Frontend DApp).<br>- **Trần Văn Nhật Minh:** Vai chính Lab 8–11: Giao diện (Frontend DApp) \| Vai chính Lab 12–15: Đặc tả (SPEC & Gate Review).<br>- **Nguyễn Hoàng Phúc:** Vai chính Lab 8–11: Kiểm thử (Test Cases) \| Vai chính Lab 12–15: Hợp đồng (Smart Contract Core). |

---

## 🚀 Luồng cốt lõi Demo (Core Workflow)

```
[1. Tạo lô đặc sản]           [2. Thêm chặng bởi đúng vai]           [3. Quét QR xem lịch sử]
  (Cơ sở sản xuất)         (Vận chuyển / Kiểm định / Điểm bán)         (Khách mua hàng)
         │                                   │                                │
         ▼                                   ▼                                ▼
- Nhập thông tin lô hàng            - Kiểm tra quyền ví on-chain       - Quét camera mã QR
- Ký giao dịch khởi tạo             - Xác thực đúng vai trò hợp lệ     - Xem timeline từng chặng
- Tự động sinh mã QR động           - Ngăn chặn mạo danh (Revert)      - Đối soát TxHash Sepolia
```

---

## 📂 Cấu trúc thư mục dự án (Chuẩn Lab 8)

```text
HueLegend/
├── README.md               # Giới thiệu sản phẩm, chuẩn 4 câu hỏi đầu ra và hướng dẫn chạy
├── AGENTS.md               # Quy ước kỹ thuật và nguyên tắc sinh mã cho công cụ AI
├── lab08.md                # Tóm tắt thực hành Lab 8 và mẫu commit nộp bài
├── docs/
│   ├── PROJECT_PLAN.md     # Kế hoạch dự án, phân công vai trò (xoay vai) và mốc công việc
│   ├── SPEC.md             # Đặc tả 4 quy tắc kiểm thử được (Ai làm gì, khi nào, giới hạn, lỗi)
│   ├── AI_JOURNAL.md       # Nhật ký AI và 5 phản biện lạm dụng kèm biện pháp xử lý rủi ro
│   ├── ECONOMIC_RULES.md   # 4 mục kinh tế: dòng tiền, chống lạm dụng, quản trị, người dùng thiệt
│   └── PRESENTATION_PLAN.md# Kịch bản demo và phân công thuyết trình bảo vệ
├── contracts/
│   ├── training/           # 4 bài mẫu học kỹ thuật cho Lab 9, 10, 13 (ClassPoint, TimeLockVault...)
│   └── project/
│       └── ProjectCore.sol # Hợp đồng thông minh cốt lõi của HueLegend (Solidity ^0.8.20, CEI)
├── test/
│   └── ProjectCore.test.js # Bộ kiểm thử tự động (bao gồm ca kiểm thử gian lận TC-03)
├── web/
│   └── index.html          # Giao diện Web3 DApp (Huế Royal Theme, sinh QR động & Timeline)
└── evidence/
    └── lab-08...lab-15/    # Biên bản, ảnh chụp màn hình và TxHash từng lab
```

---

## ⚙️ Hướng dẫn chạy và Kiểm thử

### 1. Trải nghiệm Giao diện Web3 DApp:
- Mở trực tiếp tệp [`web/index.html`](./web/index.html) bằng trình duyệt web.
- Giao diện có sẵn **Interactive Demo Engine** với dữ liệu mẫu đặc sản Huế (Mè xửng Thiên Hương, Tôm chua Trọng Tín, Trà Cung Đình) và sinh mã QR động trực tiếp.

### 2. Biên dịch Hợp đồng qua Remix IDE:
1. Mở [Remix IDE](https://remix.ethereum.org).
2. Tải tệp [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) lên Remix.
3. Chọn compiler `0.8.20`, chọn Deploy môi trường `Injected Provider - MetaMask` (Mạng Sepolia Testnet).

### 3. Chạy ca kiểm thử tự động:
```bash
npx hardhat test test/ProjectCore.test.js
```

---

## 🌐 Thông tin triển khai & Bằng chứng thực nghiệm

- **Mạng:** Ethereum Sepolia Testnet
- **Địa chỉ ví Admin / Deployer:** `0x82d022a704706B2f144863D619D7418F8a0f19A7`
- **Mã commit nộp bài:** `lab-08: khoi tao codebase nhom va dac ta v0.1`
