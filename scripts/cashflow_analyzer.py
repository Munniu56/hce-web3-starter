"""
Chuong trinh: Phan tich dong tien vi on-chain (Cashflow Analyzer)
Mon hoc: Kinh te so / Web3 Starter (ECO2432) - Lab 6
Tuan thu dac ta: SPEC.md va quy uoc AGENTS.md
Chu thich: Tieng Viet khong dau
"""

import os
import sys
import time
from datetime import datetime, timezone
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def validate_address(address: str) -> bool:
    """Kiem tra dinh dang dia chi vi Ethereum (42 ky tu, bat dau bang 0x)."""
    if not isinstance(address, str):
        return False
    if len(address) != 42 or not address.startswith("0x"):
        return False
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False


def get_api_key() -> str:
    """Doc khoa API Etherscan tu bien moi truong, khong ghi thang trong ma nguon."""
    api_key = os.environ.get("ETHERSCAN_API_KEY")
    if not api_key:
        print("[CANH BAO] Khong tim thay bien moi truong ETHERSCAN_API_KEY.")
        # Cho phep nhap tu ban phim neu chua set bien moi truong
        api_key = input("Vui long nhap khoa Etherscan API: ").strip()
    return api_key


def fetch_transactions(address: str, api_key: str, chain_id: int = 11155111) -> list:
    """
    Truy van danh sach giao dich tu Etherscan API V2 (ho tro phan trang tu dong).
    chain_id = 11155111 (Sepolia Testnet), chain_id = 1 (Ethereum Mainnet).
    """
    base_url = "https://api.etherscan.io/v2/api"
    all_transactions = []
    page = 1
    offset = 100  # So luong ban ghi tren moi trang

    print(f"[*] Dang lay du lieu giao dich cho vi: {address} tren Chain ID: {chain_id}...")

    while True:
        params = {
            "chainid": chain_id,
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": offset,
            "sort": "asc",  # Quy tac R6: sap xep thoi gian tang dan
            "apikey": api_key,
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
        except requests.RequestException as e:
            print(f"[LOI] Loi ket noi mang den Etherscan API: {e}")
            sys.exit(1)

        # Kiem tra HTTP status code theo AGENTS.md
        if response.status_code != 200:
            print(f"[LOI] HTTP error: {response.status_code} - {response.text}")
            sys.exit(1)

        data = response.json()
        status = data.get("status")
        message = data.get("message")
        result = data.get("result")

        # Xu ly cac ma loi tu Etherscan API
        if status != "1":
            if message == "No transactions found" or result == []:
                break  # Khong co giao dich hoac da lay het trang
            elif "deprecated" in str(result).lower():
                print(f"[LOI] Endpoint API bi loi thoi: {result}")
                sys.exit(1)
            elif "invalid api key" in str(result).lower():
                print(f"[LOI] Khoa API khong hop le: {result}")
                sys.exit(1)
            else:
                print(f"[THONG BAO] Ket qua API: {message} ({result})")
                break

        if not isinstance(result, list) or len(result) == 0:
            break

        all_transactions.extend(result)
        print(f"  -> Da tai trang {page} ({len(result)} giao dich)...")

        # Neu so luong tra ve nho hon offset tuc la da lay het du lieu
        if len(result) < offset:
            break

        page += 1
        time.sleep(0.25)  # Tranh vuot gioi han tan suat goi API (Rate limit)

    return all_transactions


def fetch_current_balance(address: str, api_key: str, chain_id: int = 11155111) -> float:
    """Lay so du tuc thoi hien tai cua vi de doi chieu va tinh so du khoi diem (R8)."""
    base_url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_key,
    }
    try:
        res = requests.get(base_url, params=params, timeout=10).json()
        if res.get("status") == "1":
            return int(res.get("result", 0)) / 10**18
    except Exception as e:
        print(f"[CANH BAO] Khong the lay so du hien tai: {e}")
    return 0.0


def analyze_cashflow(address: str, transactions: list, current_balance: float = 0.0) -> tuple:
    """
    Phan tich dong tien theo cac quy tac nghiep vu trong SPEC.md:
    R1 (Inflow), R2 (Outflow), R3 (Thuc tru thanh cong),
    R4 (Giao dich that bai van tru phi), R5 (Doi wei sang ETH),
    R6 (Thoi gian tang dan), R7 (Tu chuyen), R8 (So du khoi diem).
    """
    target_addr = address.lower()
    analyzed_records = []

    total_inflow = 0.0
    total_outflow = 0.0

    # Tinh toan bien dong dong tien qua tung giao dich
    deltas = []
    for tx in transactions:
        tx_from = tx.get("from", "").lower()
        tx_to = tx.get("to", "").lower() if tx.get("to") else ""
        is_error = str(tx.get("isError", "0"))

        val_wei = int(tx.get("value", 0))
        val_eth = val_wei / 10**18  # Quy tac R5

        gas_used = int(tx.get("gasUsed", 0))
        gas_price = int(tx.get("gasPrice", 0))
        fee_wei = gas_used * gas_price
        fee_eth = fee_wei / 10**18  # Quy tac R5

        tx_time = datetime.fromtimestamp(int(tx.get("timeStamp", 0)), tz=timezone.utc)
        tx_hash = tx.get("hash", "")

        tx_type = "KHONG_XAC_DINH"
        net_change = 0.0

        # Quy tac R7: Tu chuyen cho chinh minh
        if tx_from == target_addr and tx_to == target_addr:
            tx_type = "TU_CHUYEN"
            total_outflow += fee_eth
            net_change = -fee_eth

        # Quy tac R1: Dong tien vao
        elif tx_to == target_addr and is_error == "0":
            tx_type = "VAO"
            total_inflow += val_eth
            net_change = val_eth

        # Giao dich gui den nhung that bai: vi nhan khong mat gi
        elif tx_to == target_addr and is_error == "1":
            tx_type = "DEN_THAT_BAI"
            net_change = 0.0

        # Quy tac R2, R3, R4: Dong tien ra
        elif tx_from == target_addr:
            if is_error == "0":
                # Quy tac R3: Giao dich thanh cong tru ca value va fee
                tx_type = "RA"
                total_outflow += (val_eth + fee_eth)
                net_change = -(val_eth + fee_eth)
            else:
                # Quy tac R4: Giao dich that bai khong mat value, van mat phi gas
                tx_type = "RA_THAT_BAI"
                total_outflow += fee_eth
                net_change = -fee_eth

        deltas.append({
            "time": tx_time,
            "hash": tx_hash,
            "type": tx_type,
            "value_eth": val_eth,
            "fee_eth": fee_eth,
            "net_change": net_change,
        })

    # Quy tac R8: Xac dinh so du khoi diem de bieu do luon dung thuc te
    net_flow = total_inflow - total_outflow
    initial_balance = max(0.0, current_balance - net_flow) if current_balance > 0 else 0.0

    running_balance = initial_balance
    for item in deltas:
        running_balance += item["net_change"]
        analyzed_records.append({
            **item,
            "balance_eth": max(0.0, running_balance),
        })

    summary = {
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "initial_balance": initial_balance,
        "closing_balance": running_balance,
        "tx_count": len(analyzed_records),
    }

    return analyzed_records, summary


def generate_chart(records: list, summary: dict, address: str, output_path: str = "balance_chart.png"):
    """Ve bieu do duong bien dong so du theo thoi gian va luu file anh."""
    if not records:
        print("[CANH BAO] Khong co du lieu de ve bieu do.")
        return

    times = [r["time"] for r in records]
    balances = [r["balance_eth"] for r in records]

    plt.figure(figsize=(11, 5.5), dpi=150)
    plt.plot(times, balances, marker="o", markersize=3.5, linestyle="-", color="#1a73e8", linewidth=2, label="So du luy ke (ETH)")

    # To mau vung duoi duong bieu dien
    plt.fill_between(times, balances, color="#1a73e8", alpha=0.15)

    short_addr = f"{address[:6]}...{address[-4:]}"
    plt.title(f"Bieu do bien dong so du vi {short_addr} (Sepolia Testnet)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Thoi gian (UTC)", fontsize=11)
    plt.ylabel("So du (ETH)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Format truc thoi gian
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate()

    # Chu thich thong tin tong hop tren bieu do
    info_box = (
        f"Tong vao: {summary['total_inflow']:,.4f} ETH\n"
        f"Tong ra: {summary['total_outflow']:,.4f} ETH\n"
        f"So du cuoi: {summary['closing_balance']:,.4f} ETH"
    )
    plt.gca().text(
        0.02, 0.95, info_box,
        transform=plt.gca().transAxes,
        fontsize=9.5,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#ced4da", alpha=0.9)
    )

    plt.legend(loc="upper right")
    plt.tight_layout()

    # Tao thu muc neu chua ton tai
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"[OK] Da luu bieu do thanh cong tai: {output_path}")


def main():
    print("=" * 70)
    print("  HE THONG PHAN TICH DONG TIEN VI ON-CHAIN (LAB 6 - ECO2432)")
    print("=" * 70)

    # 1. Doc khoa API tu bien moi truong (Quy tac bao mat AGENTS.md)
    api_key = get_api_key()
    if not api_key:
        print("[LOI] Yeu cau khoa Etherscan API de tiep tuc.")
        sys.exit(1)

    # 2. Xac dinh dia chi vi kiem thu
    default_address = "0x5856B2C7e636d7A0b1FE25004eF9D6D158BE8B01"
    address = sys.argv[1] if len(sys.argv) > 1 else default_address

    if not validate_address(address):
        print(f"[LOI E4] Dia chi vi khong hop le: {address}")
        sys.exit(1)

    print(f"[+] Dia chi vi kiem thu: {address}")
    chain_id = 11155111  # Sepolia

    # 3. Lay du lieu giao dich va so du hien tai
    txs = fetch_transactions(address, api_key, chain_id=chain_id)
    if not txs:
        print("[THONG BAO E1] Vi khong co giao dich trong ky.")
        return

    current_bal = fetch_current_balance(address, api_key, chain_id=chain_id)

    # 4. Phan tich dong tien
    records, summary = analyze_cashflow(address, txs, current_balance=current_bal)

    # 5. In ket qua ra console
    print("\n" + "=" * 70)
    print("  KET QUA PHAN TICH DONG TIEN (SUMMARY METRICS)")
    print("=" * 70)
    print(f"  Tong so giao dich: {summary['tx_count']}")
    print(f"  Tong tien vao (Total Inflow):    {summary['total_inflow']:15.6f} ETH")
    print(f"  Tong tien ra  (Total Outflow):   {summary['total_outflow']:15.6f} ETH")
    print(f"  Bien dong rong (Net Change):     {(summary['total_inflow'] - summary['total_outflow']):15.6f} ETH")
    print(f"  So du cuoi ky (Closing Balance): {summary['closing_balance']:15.6f} ETH")
    print("=" * 70)

    print("\n[+] 10 giao dich gan nhat:")
    print(f"{'Thoi gian (UTC)':<20} | {'Loai':<12} | {'Gia tri (ETH)':<14} | {'Phi (ETH)':<12} | {'So du (ETH)'}")
    print("-" * 75)
    for r in records[-10:]:
        t_str = r['time'].strftime("%Y-%m-%d %H:%M")
        print(f"{t_str:<20} | {r['type']:<12} | {r['value_eth']:<14.6f} | {r['fee_eth']:<12.6f} | {r['balance_eth']:.6f}")

    # 6. Xuat bieu do
    output_chart = os.path.join("Lab 1-7", "balance_chart.png")
    generate_chart(records, summary, address, output_chart)


if __name__ == "__main__":
    main()
