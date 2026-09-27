# -*- coding: utf-8 -*-
"""
analyze_wallet.py — Phan tich dong tien ETH cua vi Ethereum
Thuc hien dung dac ta SPEC.md (Lab 5 / Lab 6) — ECO2432
Tac gia: Ngo Thi Thuy Van — 23K4300023 — Lop K57 - Kinh te so
Python 3.10+

Cach chay:
    Windows PowerShell:
        $env:ETHERSCAN_API_KEY = "your_key_here"
        python analyze_wallet.py 0xYourAddress
        # Hoac phan tich mang Sepolia:
        python analyze_wallet.py 0xYourAddress --chainid 11155111

    Linux / macOS:
        export ETHERSCAN_API_KEY="your_key_here"
        python analyze_wallet.py 0xYourAddress
"""

import os
import sys
import re
import time
import argparse
import datetime
from typing import Optional

# Dam bao tuong thich ma hoa ky tu UTF-8 tren Windows PowerShell / CMD
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thu vien ben ngoai
try:
    import requests
    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except ImportError as e:
    print(f"[LOI] Thieu thu vien: {e}")
    print("Chay lenh: pip install requests pandas matplotlib")
    sys.exit(1)

# ─────────────────────────────────────────────
# HANG SO CAU HINH
# ─────────────────────────────────────────────
ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"  # API v2 — chuan hoa da mang theo Etherscan 2026
WEI_PER_ETH = 10 ** 18                                  # R5: he so quy doi wei sang ETH
PAGE_SIZE = 10_000                                       # E3: so ban ghi toi da moi trang
MAX_PAGES = 100                                          # Gioi han an toan tranh vong lap vo han


# ─────────────────────────────────────────────
# KIEM TRA DAU VAO (E4)
# ─────────────────────────────────────────────
def validate_address(address: str) -> str:
    """
    Kiem tra dinh dang dia chi vi Ethereum theo chuan EIP-55.
    Yeu cau: 42 ky tu, bat dau '0x', phan con lai la hex hop le.
    Tra ve dia chi chu thuong chuan hoa de so sanh khong phan biet hoa/thuong.
    Neu sai: in thong bao E4 va thoat chuong trinh.
    """
    pattern = re.compile(r"^0x[0-9a-fA-F]{40}$")
    if not pattern.match(address):
        print("Dia chi vi khong hop le theo chuan EIP-55")
        sys.exit(1)
    return address.lower()


# ─────────────────────────────────────────────
# DOC KHOA API TU BIEN MOI TRUONG (AGENTS.md quy tac 1)
# ─────────────────────────────────────────────
def get_api_key() -> str:
    """
    Doc ETHERSCAN_API_KEY tu bien moi truong.
    Tuyet doi KHONG ghi khoa API vao ma nguon theo quy uoc AGENTS.md.
    """
    key = os.environ.get("ETHERSCAN_API_KEY", "").strip()
    if not key:
        print("[LOI] Bien moi truong ETHERSCAN_API_KEY chua duoc dat.")
        print("Windows PowerShell: $env:ETHERSCAN_API_KEY = 'your_key'")
        print("Linux / macOS     : export ETHERSCAN_API_KEY='your_key'")
        sys.exit(1)
    return key


# ─────────────────────────────────────────────
# GOI API ETHERSCAN VOI XU LY LOI (E2)
# ─────────────────────────────────────────────
def etherscan_get(params: dict, api_key: str, chain_id: int) -> dict:
    """
    Thuc hien mot yeu cau GET den Etherscan API v2.
    Kiem tra trang thai phan hoi HTTP truoc khi xu ly (AGENTS.md quy tac 2).
    Xu ly E2: NOTOK, Invalid API Key, rate limit.
    """
    params["chainid"] = chain_id
    params["apikey"] = api_key

    try:
        response = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=30)
    except requests.exceptions.ConnectionError:
        print("[LOI] Khong the ket noi den Etherscan. Kiem tra ket noi mang.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[LOI] Yeu cau bi timeout. Thu lai sau.")
        sys.exit(1)

    # Kiem tra HTTP status
    if response.status_code != 200:
        print(f"[LOI] HTTP {response.status_code}: {response.text[:200]}")
        sys.exit(1)

    data = response.json()
    status = data.get("status", "")
    message = data.get("message", "")
    result = data.get("result", "")

    # Xu ly E2: Etherscan tra ve loi
    if status == "0":
        # Danh sach rong la hop le — de tang duoi xu ly E1
        if message == "No transactions found" or result == []:
            return data
        # Cac loi thuc su: khoa API sai, het han muc, v.v.
        print(f"[LOI] Etherscan API: status={status} | message={message} | result={result}")
        sys.exit(1)

    return data


# ─────────────────────────────────────────────
# LAY SO DU HIEN TAI CUA VI
# ─────────────────────────────────────────────
def fetch_balance(address: str, api_key: str, chain_id: int) -> float:
    """
    Tra ve so du hien tai cua vi tinh bang ETH.
    Dung de tinh so du dau ky theo R8.
    """
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
    }
    data = etherscan_get(params, api_key, chain_id)
    try:
        balance_wei = int(data["result"])
    except (ValueError, TypeError):
        balance_wei = 0
    return balance_wei / WEI_PER_ETH  # R5: quy doi wei sang ETH


# ─────────────────────────────────────────────
# LAY DANH SACH GIAO DICH — PHAN TRANG TU DONG (E3)
# ─────────────────────────────────────────────
def fetch_transactions(address: str, api_key: str, chain_id: int, start_ts: int, end_ts: int) -> list[dict]:
    """
    Lay toan bo giao dich ETH thuong (normal txlist) cua dia chi trong khoang thoi gian.
    Su dung sort='desc' de lay tu giao dich moi nhat ve qua khu,
    giup tranh loi bi mac ket o cac giao dich cu tu nhieu nam truoc.
    """
    collected_txs: list[dict] = []
    page = 1

    print(f"  Dang tai giao dich ({PAGE_SIZE} ban ghi/trang, toi da {MAX_PAGES} trang)...")

    reached_before_start = False

    while page <= MAX_PAGES and not reached_before_start:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99_999_999,
            "page": page,
            "offset": PAGE_SIZE,
            "sort": "desc",  # Lay tu moi nhat ve cu nhat
        }

        data = etherscan_get(params, api_key, chain_id)
        message = data.get("message", "")
        result = data.get("result", [])

        if not result or message == "No transactions found":
            break

        for tx in result:
            tx_ts = int(tx["timeStamp"])
            if tx_ts > end_ts:
                continue
            elif tx_ts < start_ts:
                reached_before_start = True
                break
            else:
                collected_txs.append(tx)

        print(f"    Trang {page}: {len(result)} ban ghi lay ve, trong ky: {len(collected_txs)}")

        if len(result) < PAGE_SIZE:
            break

        page += 1
        time.sleep(0.22)  # Gioi han tan suat Etherscan free tier (5 req/s)

    # R6: Sap xep tang dan theo thoi gian truoc khi xu ly
    collected_txs.sort(key=lambda x: int(x["timeStamp"]))
    print(f"  Tong giao dich trong ky da loc (R6): {len(collected_txs)}")
    return collected_txs


# ─────────────────────────────────────────────
# XU LY GIAO DICH THEO QUY TAC NGHIEP VU R1-R8
# ─────────────────────────────────────────────
def process_transactions(txs: list[dict], address: str, initial_balance: float) -> "pd.DataFrame":
    """
    Ap dung cac quy tac R1-R8 de phan loai dong tien va tinh so du luy ke.
    """
    records = []
    balance = initial_balance

    for tx in txs:
        ts          = int(tx["timeStamp"])
        tx_hash     = tx["hash"]
        from_addr   = tx["from"].lower()
        to_addr     = tx["to"].lower() if tx.get("to") else ""
        value_wei   = int(tx.get("value", 0))
        gas_used    = int(tx.get("gasUsed", 0))
        gas_price   = int(tx.get("gasPrice", 0))
        is_error    = str(tx.get("isError", "0"))

        # R5: Quy doi wei sang ETH truoc khi tinh toan
        fee_eth   = (gas_used * gas_price) / WEI_PER_ETH
        value_eth = value_wei / WEI_PER_ETH

        is_from_me = (from_addr == address)
        is_to_me   = (to_addr == address)

        # ── R7: Giao dich tu chuyen cho chinh minh (from == to) ──
        if is_from_me and is_to_me:
            balance -= fee_eth
            records.append({
                "timestamp"   : ts,
                "tx_hash"     : tx_hash,
                "flow_type"   : "RA",
                "amount_eth"  : 0.0,
                "fee_eth"     : fee_eth,
                "balance_eth" : balance,
                "note"        : "self-transfer",
            })
            continue

        # ── R1: Tien vao (Inflow) ──
        if is_to_me and is_error == "0":
            balance += value_eth
            records.append({
                "timestamp"   : ts,
                "tx_hash"     : tx_hash,
                "flow_type"   : "VAO",
                "amount_eth"  : value_eth,
                "fee_eth"     : 0.0,
                "balance_eth" : balance,
                "note"        : "inflow",
            })

        # ── R2 + R3 + R4: Tien ra (Outflow) ──
        elif is_from_me:
            if is_error == "0":
                # R3: Giao dich thanh cong — tru ca value lan phi gas
                balance -= (value_eth + fee_eth)
                records.append({
                    "timestamp"   : ts,
                    "tx_hash"     : tx_hash,
                    "flow_type"   : "RA",
                    "amount_eth"  : value_eth,
                    "fee_eth"     : fee_eth,
                    "balance_eth" : balance,
                    "note"        : "outflow-ok",
                })
            else:
                # R4: Giao dich that bai — value duoc hoan lai, NHUNG phi gas van bi tru
                balance -= fee_eth
                records.append({
                    "timestamp"   : ts,
                    "tx_hash"     : tx_hash,
                    "flow_type"   : "RA",
                    "amount_eth"  : 0.0,
                    "fee_eth"     : fee_eth,
                    "balance_eth" : balance,
                    "note"        : "outflow-failed",
                })

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    # R6: Dam bao sap xep tang dan theo thoi gian
    df.sort_values("timestamp", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    return df


# ─────────────────────────────────────────────
# VE BIEU DO DUONG SO DU LUY KE
# ─────────────────────────────────────────────
def plot_balance_chart(df: "pd.DataFrame", address: str, days: int) -> str:
    """
    Ve bieu do duong the hien bien dong so du ETH luy ke theo thoi gian.
    Luu file PNG va tra ve duong dan file.
    """
    if df.empty:
        print("Khong co du lieu de ve bieu do.")
        return ""

    fig, ax = plt.subplots(figsize=(14, 6))

    # Duong so du chinh
    ax.plot(
        df["datetime"], df["balance_eth"],
        color="#2563EB", linewidth=1.8, label="So du ETH luy ke", zorder=3
    )
    ax.fill_between(df["datetime"], df["balance_eth"], alpha=0.10, color="#2563EB")

    # Danh dau diem giao dich VAO (xanh la) va RA (do)
    inflow  = df[df["flow_type"] == "VAO"]
    outflow = df[df["flow_type"] == "RA"]

    if not inflow.empty:
        ax.scatter(inflow["datetime"], inflow["balance_eth"],
                   color="#16A34A", s=40, zorder=5, label="Tien vao (VAO)", alpha=0.85)
    if not outflow.empty:
        ax.scatter(outflow["datetime"], outflow["balance_eth"],
                   color="#DC2626", s=30, zorder=5, label="Tien ra (RA)", alpha=0.75)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha="right")

    ax.set_title(
        f"Bieu do so du ETH luy ke — {days} ngay gan nhat\n"
        f"Vi: {address[:8]}...{address[-6:]}",
        fontsize=13, fontweight="bold", pad=14
    )
    ax.set_xlabel("Thoi gian (UTC)", fontsize=11)
    ax.set_ylabel("So du (ETH)", fontsize=11)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.35)

    plt.tight_layout()

    # Luu file PNG tai thu muc hien tai
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "bieu_do_so_du_lab06.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\n  [THANH CONG] Bieu do da luu: {out_path}")
    plt.close()
    return out_path


# ─────────────────────────────────────────────
# IN BANG GIAO DICH CHI TIET
# ─────────────────────────────────────────────
def print_transaction_table(df: "pd.DataFrame") -> None:
    if df.empty:
        return

    header = (
        f"{'Thoi gian (UTC)':<22} {'Tx Hash':<18} {'Loai':<6} "
        f"{'So tien (ETH)':>16} {'Phi gas (ETH)':>14} {'So du luy ke (ETH)':>20} {'Ghi chu'}"
    )
    sep = "=" * 108

    print(f"\n{sep}\n{header}\n{sep}")

    for _, row in df.iterrows():
        dt_str     = row["datetime"].strftime("%Y-%m-%d %H:%M:%S")
        hash_short = f"{row['tx_hash'][:8]}...{row['tx_hash'][-6:]}"
        loai       = row["flow_type"]

        print(
            f"{dt_str:<22} {hash_short:<18} {loai:<6} "
            f"{row['amount_eth']:>16.8f} {row['fee_eth']:>14.8f} "
            f"{row['balance_eth']:>20.8f} {row.get('note', '')}"
        )

    print(sep)
    print(f"Tong so giao dich hien thi: {len(df)}")


# ─────────────────────────────────────────────
# IN 3 CHI SO TONG HOP
# ─────────────────────────────────────────────
def print_summary(df: "pd.DataFrame", current_balance: float) -> None:
    if df.empty:
        return

    total_inflow = df.loc[df["flow_type"] == "VAO", "amount_eth"].sum()
    out_rows      = df[df["flow_type"] == "RA"]
    total_outflow = (out_rows["amount_eth"] + out_rows["fee_eth"]).sum()

    print("\n" + "-" * 54)
    print("  CHI SO TONG HOP (SUMMARY METRICS)")
    print("-" * 54)
    print(f"  Tong tien vao (Total Inflow)  : {total_inflow:>16.8f} ETH")
    print(f"  Tong tien ra  (Total Outflow) : {total_outflow:>16.8f} ETH")
    print(f"  So du cuoi ky (Closing Bal.)  : {current_balance:>16.8f} ETH")
    print(f"  Bien dong rong (Net Flow)     : {total_inflow - total_outflow:>+16.8f} ETH")
    print("-" * 54)


# ─────────────────────────────────────────────
# HAM CHINH
# ─────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phan tich dong tien ETH cua vi Ethereum — ECO2432 Lab 6",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("address", help="Dia chi vi Ethereum (42 ky tu, bat dau 0x)")
    parser.add_argument("--days", type=int, default=90,
                        help="So ngay phan tich ke tu hom nay (mac dinh: 90)")
    parser.add_argument("--chainid", type=int, default=1,
                        help="Chain ID mang luoi: 1 (Mainnet - mac dinh), 11155111 (Sepolia)")
    args = parser.parse_args()

    # Buoc 1: Kiem tra E4
    address = validate_address(args.address)
    days    = args.days
    chain_id = args.chainid

    # Buoc 2: Doc khoa API
    api_key = get_api_key()

    # Buoc 3: Tinh khoang thoi gian
    now_ts   = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    start_ts = now_ts - days * 86_400

    start_date = datetime.datetime.fromtimestamp(start_ts, datetime.timezone.utc).strftime("%Y-%m-%d")
    print(f"\n{'=' * 54}")
    print(f"  Phan tich vi  : {address}")
    print(f"  Mang luoi     : Chain ID {chain_id}")
    print(f"  Khoang thoi gian: {days} ngay ({start_date} -> hom nay)")
    print(f"{'=' * 54}")

    # Buoc 4: Lay so du hien tai (R8)
    print("\n[1/3] Lay so du hien tai cua vi...")
    current_balance = fetch_balance(address, api_key, chain_id)
    print(f"  So du hien tai: {current_balance:.8f} ETH")

    # Buoc 5: Lay giao dich co phan trang (E3)
    print("\n[2/3] Tai danh sach giao dich...")
    txs = fetch_transactions(address, api_key, chain_id, start_ts, now_ts)

    # Buoc 6: Xu ly E1
    if not txs:
        print("\nVi khong co giao dich trong ky")
        sys.exit(0)

    # Buoc 7: Tinh so du dau ky theo R8
    print("\n[3/3] Xu ly giao dich va tinh toan...")
    temp_df = process_transactions(txs, address, initial_balance=0.0)

    if not temp_df.empty:
        tmp_inflow   = temp_df.loc[temp_df["flow_type"] == "VAO", "amount_eth"].sum()
        tmp_out_rows = temp_df[temp_df["flow_type"] == "RA"]
        tmp_outflow  = (tmp_out_rows["amount_eth"] + tmp_out_rows["fee_eth"]).sum()
        net_flow     = tmp_inflow - tmp_outflow
        initial_balance = current_balance - net_flow
        print(f"  Dong tien rong trong ky (R8): {net_flow:+.8f} ETH")
        print(f"  So du dau ky tinh duoc  (R8): {initial_balance:.8f} ETH")
    else:
        initial_balance = current_balance

    # Buoc 8: Xu ly voi initial_balance chinh xac
    df = process_transactions(txs, address, initial_balance=initial_balance)

    # Buoc 9: Hien thi
    print_transaction_table(df)
    print_summary(df, current_balance)

    # Buoc 10: Ve bieu do
    plot_balance_chart(df, address, days)

    print("\n  Hoan thanh phan tich!")


if __name__ == "__main__":
    main()
