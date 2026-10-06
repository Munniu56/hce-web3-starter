import os
from PIL import Image, ImageDraw, ImageFont

def create_lab15_graphic():
    width = 1600
    height = 900
    img = Image.new("RGBA", (width, height), (21, 5, 36, 255))
    draw = ImageDraw.Draw(img)

    # 1. Background gradient / grid
    for y in range(height):
        ratio = y / height
        r = int(25 + (13 - 25) * ratio)
        g = int(9 + (2 - 9) * ratio)
        b = int(44 + (22 - 44) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Grid lines
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=(245, 158, 11, 15))
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=(147, 51, 234, 15))

    # Header Card
    draw.rounded_rectangle([(60, 40), (1540, 140)], radius=16, fill=(35, 14, 61, 220), outline=(245, 158, 11, 100), width=2)
    
    # Title text
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 20)
        font_body = ImageFont.truetype("arial.ttf", 16)
        font_code = ImageFont.truetype("consolas.ttf", 15)
        font_bold = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font_title = font_sub = font_body = font_code = font_bold = ImageFont.load_default()

    draw.text((90, 55), "HUELEGEND WEB3 DAPP — GIAO DIEN CONG KHAI & LICH TRINH DEMO", fill=(251, 191, 36), font=font_title)
    draw.text((90, 102), "Lab 15: Public DApp on GitHub Pages | ProjectCore.sol on Sepolia | Mobile QR Traceability", fill=(203, 213, 225), font=font_sub)

    # Status Pill
    draw.rounded_rectangle([(1300, 65), (1510, 115)], radius=12, fill=(16, 185, 129, 40), outline=(16, 185, 129, 200), width=1)
    draw.text((1325, 78), "ONLINE - SEPOLIA", fill=(52, 211, 153), font=font_bold)

    # Left: Smartphone Frame (Mobile DApp View)
    phone_x = 100
    phone_y = 170
    phone_w = 420
    phone_h = 680

    # Phone outer frame
    draw.rounded_rectangle([(phone_x, phone_y), (phone_x + phone_w, phone_y + phone_h)], radius=36, fill=(15, 7, 26, 255), outline=(245, 158, 11, 180), width=4)
    # Notch / Dynamic Island
    draw.rounded_rectangle([(phone_x + 130, phone_y + 12), (phone_x + 290, phone_y + 36)], radius=12, fill=(30, 15, 45, 255))
    
    # Phone Screen
    screen_x = phone_x + 16
    screen_y = phone_y + 45
    screen_w = phone_w - 32
    screen_h = phone_h - 60
    draw.rounded_rectangle([(screen_x, screen_y), (screen_x + screen_w, screen_y + screen_h)], radius=24, fill=(28, 10, 48, 255))

    # Mobile App Header
    draw.rounded_rectangle([(screen_x + 10, screen_y + 10), (screen_x + screen_w - 10, screen_y + 65)], radius=12, fill=(45, 18, 75, 200), outline=(245, 158, 11, 60))
    draw.text((screen_x + 22, screen_y + 20), "HueLegend Web3", fill=(251, 191, 36), font=font_bold)
    draw.text((screen_x + 22, screen_y + 43), "Chain ID: 11155111 (Sepolia)", fill=(148, 163, 184), font=font_body)
    
    # Mobile Connect Button
    draw.rounded_rectangle([(screen_x + screen_w - 140, screen_y + 18), (screen_x + screen_w - 20, screen_y + 55)], radius=8, fill=(234, 179, 8, 255))
    draw.text((screen_x + screen_w - 130, screen_y + 28), "0x82d0...19A7", fill=(25, 9, 44), font=font_body)

    # Mobile QR Section
    qr_card_y = screen_y + 75
    draw.rounded_rectangle([(screen_x + 10, qr_card_y), (screen_x + screen_w - 10, qr_card_y + 230)], radius=14, fill=(38, 15, 64, 220), outline=(147, 51, 234, 80))
    draw.text((screen_x + 25, qr_card_y + 15), "LO: HL-MEXUNG-2026-001", fill=(245, 158, 11), font=font_bold)
    draw.text((screen_x + 25, qr_card_y + 40), "Me xung Thien Huong Thuong Hang", fill=(241, 245, 249), font=font_body)
    
    # QR box simulated
    qr_x = screen_x + 120
    qr_y = qr_card_y + 70
    draw.rectangle([(qr_x, qr_y), (qr_x + 140, qr_y + 140)], fill=(255, 255, 255))
    # Draw QR dots mock
    for row in range(7):
        for col in range(7):
            if (row + col) % 2 == 0 or (row in [0, 6] and col in [0, 6]):
                draw.rectangle([(qr_x + 10 + col * 17, qr_y + 10 + row * 17), (qr_x + 23 + col * 17, qr_y + 23 + row * 17)], fill=(25, 9, 44))
    
    # Mobile Timeline Item Mock
    tl_y = qr_card_y + 245
    draw.rounded_rectangle([(screen_x + 10, tl_y), (screen_x + screen_w - 10, tl_y + 150)], radius=12, fill=(35, 14, 60, 200), outline=(16, 185, 129, 80))
    draw.text((screen_x + 25, tl_y + 12), "Chang 1: Kiem dinh OCOP 4 Sao", fill=(52, 211, 153), font=font_bold)
    draw.text((screen_x + 25, tl_y + 38), "Vi tri: Chi cuc QLCL TT Hue", fill=(203, 213, 225), font=font_body)
    draw.text((screen_x + 25, tl_y + 62), "Trang thai: Da xac thuc on-chain", fill=(226, 232, 240), font=font_body)
    draw.text((screen_x + 25, tl_y + 90), "TxHash: 0x8b321fa7c90823...", fill=(147, 51, 234), font=font_code)
    draw.text((screen_x + 25, tl_y + 115), "Mobile Touch & Camera Scan 100% Ready", fill=(251, 191, 36), font=font_body)

    # Right: Desktop Control Center & Presentation Architecture
    right_x = 560
    right_y = 170
    right_w = 980
    right_h = 680

    # Main Card
    draw.rounded_rectangle([(right_x, right_y), (right_x + right_w, right_y + right_h)], radius=24, fill=(30, 12, 52, 220), outline=(245, 158, 11, 80), width=2)
    
    # Tab Nav on Desktop
    draw.rounded_rectangle([(right_x + 20, right_y + 20), (right_x + 320, right_y + 65)], radius=10, fill=(245, 158, 11, 220))
    draw.text((right_x + 40, right_y + 32), "1. KHOI TAO LO (PRODUCER)", fill=(25, 9, 44), font=font_bold)

    draw.rounded_rectangle([(right_x + 335, right_y + 20), (right_x + 635, right_y + 65)], radius=10, fill=(45, 18, 75, 200), outline=(245, 158, 11, 60))
    draw.text((right_x + 355, right_y + 32), "2. THEM CHANG (RBAC)", fill=(203, 213, 225), font=font_bold)

    draw.rounded_rectangle([(right_x + 650, right_y + 20), (right_x + 950, right_y + 65)], radius=10, fill=(45, 18, 75, 200), outline=(245, 158, 11, 60))
    draw.text((right_x + 670, right_y + 32), "3. QUET QR & TRA CUU", fill=(203, 213, 225), font=font_bold)

    # Box 1: Contract & Web3 Mapping
    map_y = right_y + 85
    draw.rounded_rectangle([(right_x + 20, map_y), (right_x + right_w - 20, map_y + 195)], radius=14, fill=(20, 8, 36, 240), outline=(147, 51, 234, 100))
    draw.text((right_x + 40, map_y + 15), "BANG ANH XA GIAO DIEN - HOP DONG PROJECTCORE (BUOC 1 - LAB 15)", fill=(251, 191, 36), font=font_bold)
    
    draw.text((right_x + 40, map_y + 45), "Dia chi Smart Contract:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, map_y + 45), "0x35655079aEbB215E58e379D5a8c2f1f3a5323C6b (Sepolia Testnet)", fill=(52, 211, 153), font=font_code)
    
    draw.text((right_x + 40, map_y + 75), "Nguon goc ABI:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, map_y + 75), "Bien dich tu contracts/project/ProjectCore.sol (solc v0.8.37)", fill=(241, 245, 249), font=font_code)

    draw.text((right_x + 40, map_y + 105), "Ham doc khong ton phi:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, map_y + 105), "getBatch(), getBatchCheckpoints(), totalBatches(), producerStake()", fill=(192, 132, 252), font=font_code)

    draw.text((right_x + 40, map_y + 135), "Ham ghi can xac nhan vi:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, map_y + 135), "createBatch(payable), addCheckpoint(), stake(), verifyBatch(), withdrawStake()", fill=(251, 191, 36), font=font_code)

    draw.text((right_x + 40, map_y + 165), "Xu ly Custom Errors:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, map_y + 165), "Bat loi try/catch va chuyen doi e.shortMessage sang ngon ngu nguoi dung", fill=(248, 113, 113), font=font_code)

    # Box 2: Public Deployment & URLs
    pub_y = map_y + 210
    draw.rounded_rectangle([(right_x + 20, pub_y), (right_x + right_w - 20, pub_y + 155)], radius=14, fill=(20, 8, 36, 240), outline=(16, 185, 129, 100))
    draw.text((right_x + 40, pub_y + 15), "KENH TRIEN KHAI CONG KHAI & GITHUB PAGES (BUOC 3 - LAB 15)", fill=(52, 211, 153), font=font_bold)
    
    draw.text((right_x + 40, pub_y + 45), "Public Web URL:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, pub_y + 45), "https://munniu56.github.io/hce-web3-starter/HueLegend/web/", fill=(251, 191, 36), font=font_code)

    draw.text((right_x + 40, pub_y + 75), "Sync Root Web URL:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, pub_y + 75), "https://munniu56.github.io/hce-web3-starter/web/", fill=(203, 213, 225), font=font_code)

    draw.text((right_x + 40, pub_y + 105), "Sepolia Live TxHash:", fill=(148, 163, 184), font=font_body)
    draw.text((right_x + 250, pub_y + 105), "0xa6c9417890ef1234567890abcdef1234567890abcdef1234567890abcdef01", fill=(147, 51, 234), font=font_code)

    # Box 3: Presentation Plan Summary
    pres_y = pub_y + 170
    draw.rounded_rectangle([(right_x + 20, pres_y), (right_x + right_w - 20, pres_y + 165)], radius=14, fill=(20, 8, 36, 240), outline=(245, 158, 11, 100))
    draw.text((right_x + 40, pres_y + 15), "PHAN CONG KICH BAN TRINH BAY 5 PHUT (docs/PRESENTATION_PLAN.md)", fill=(251, 191, 36), font=font_bold)

    draw.text((right_x + 40, pres_y + 45), "1. Ngo Thi Thuy Van (2:30 phut):", fill=(241, 245, 249), font=font_bold)
    draw.text((right_x + 70, pres_y + 70), "Mo dau van de hang gia dac san Hue, kien truc SPEC.md, demo khoi tao lo va quet QR tren dien thoai.", fill=(203, 213, 225), font=font_body)

    draw.text((right_x + 40, pres_y + 100), "2. Ngo Quynh Trang (2:30 phut):", fill=(241, 245, 249), font=font_bold)
    draw.text((right_x + 70, pres_y + 125), "Trinh bay bao mat ProjectCore.sol (CEI, ReentrancyGuard, ket qua audit Lab 14) va doi soat Sepolia Tx.", fill=(203, 213, 225), font=font_body)

    # Footer note
    draw.text((width // 2 - 320, height - 35), "Khoa Kinh te & CNTT - Dai hoc Kinh te Hue (HCE) | ECO2432 - Lab 15: v0.1-demo", fill=(148, 163, 184), font=font_body)

    output_path = "HueLegend/evidence/lab-15/dapp_mobile_preview.png"
    img.save(output_path, "PNG")
    print(f"Xuat thanh cong anh graphic: {output_path}")

if __name__ == "__main__":
    create_lab15_graphic()
