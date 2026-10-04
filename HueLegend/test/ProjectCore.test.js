const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("HueLegend - ProjectCore (Traceability & Post-Audit Test Suite)", function () {
  let projectCore;
  let owner, producer, logistics, retailer, inspector, attacker;

  const BATCH_CODE = "HL-MEXUNG-2026-001";
  const PRODUCT_NAME = "Me Xung Thien Huong Thuong Hang";
  const ORIGIN = "Phu Hau, TP Hue";
  const INITIAL_URI = "ipfs://QmHueMeXungOCOP4StarBatch001";
  const STAKE_AMOUNT = ethers.parseEther("0.05");

  beforeEach(async function () {
    [owner, producer, logistics, retailer, inspector, attacker] = await ethers.getSigners();

    const ProjectCoreFactory = await ethers.getContractFactory("ProjectCore");
    projectCore = await ProjectCoreFactory.deploy();
    await projectCore.waitForDeployment();

    // Cap quyen vai tro cho cac ben tham gia chuoi cung ung HueLegend
    const ROLE_PRODUCER = await projectCore.ROLE_PRODUCER();
    const ROLE_LOGISTICS = await projectCore.ROLE_LOGISTICS();
    const ROLE_RETAILER = await projectCore.ROLE_RETAILER();
    const ROLE_INSPECTOR = await projectCore.ROLE_INSPECTOR();

    await projectCore.grantRole(producer.address, ROLE_PRODUCER);
    await projectCore.grantRole(logistics.address, ROLE_LOGISTICS);
    await projectCore.grantRole(retailer.address, ROLE_RETAILER);
    await projectCore.grantRole(inspector.address, ROLE_INSPECTOR);

    // Co so san xuat nap tien ky quy cam ket chat luong (0.05 ETH)
    await projectCore.connect(producer).depositStake({ value: STAKE_AMOUNT });
  });

  // ================= CA KIEM THU 1: HOP LE (CREATION) =================
  it("TC-01: Co so da nap coc tao lo hang thanh cong va phat event", async function () {
    await expect(
      projectCore.connect(producer).createBatch(
        BATCH_CODE,
        PRODUCT_NAME,
        ORIGIN,
        INITIAL_URI
      )
    )
      .to.emit(projectCore, "BatchCreated")
      .withArgs(BATCH_CODE, PRODUCT_NAME, producer.address, (val) => val > 0);

    const batch = await projectCore.getBatch(BATCH_CODE);
    expect(batch.batchCode).to.equal(BATCH_CODE);
    expect(batch.productName).to.equal(PRODUCT_NAME);
    expect(batch.origin).to.equal(ORIGIN);
    expect(batch.producer).to.equal(producer.address);
    expect(batch.isVerified).to.be.false;

    const checkpoints = await projectCore.getCheckpoints(BATCH_CODE);
    expect(checkpoints.length).to.equal(1);
    expect(checkpoints[0].location).to.equal(ORIGIN);
  });

  // ================= KIEM TRA VÁ LỖI 1: RÀNG BUỘC TIỀN CỌC KHI TẠO LÔ =================
  it("TC-01b (Va loi 1): Co so chua nap du coc bi revert StakeTooLow khi tao lo", async function () {
    const [, , , , , , poorProducer] = await ethers.getSigners();
    const ROLE_PRODUCER = await projectCore.ROLE_PRODUCER();
    await projectCore.grantRole(poorProducer.address, ROLE_PRODUCER);

    // Thu tao lo khi chua nap coc 0.05 ETH -> Phai bi revert
    await expect(
      projectCore.connect(poorProducer).createBatch(
        "HL-FAKE-001",
        "Me Xung Chua Nap Coc",
        "Hue",
        ""
      )
    ).to.be.revertedWithCustomError(projectCore, "StakeTooLow");
  });

  // ================= CA KIEM THU 2: HOP LE (CHECKPOINT BY ROLE) =================
  it("TC-02: Don vi van chuyen (dung vai tro) them chang hanh trinh thanh cong", async function () {
    await projectCore.connect(producer).createBatch(
      BATCH_CODE,
      PRODUCT_NAME,
      ORIGIN,
      INITIAL_URI
    );

    const ROLE_LOGISTICS = await projectCore.ROLE_LOGISTICS();
    const LOCATION = "Ga Hue, Phuong Duc, TP Hue";
    const ACTION = "Xuat kho van chuyen di Ha Noi qua duong sat";
    const META_URI = "ipfs://QmLogisticsShipmentReceipt001";

    await expect(
      projectCore.connect(logistics).addCheckpoint(
        BATCH_CODE,
        ROLE_LOGISTICS,
        LOCATION,
        ACTION,
        META_URI
      )
    )
      .to.emit(projectCore, "CheckpointAdded")
      .withArgs(BATCH_CODE, logistics.address, ROLE_LOGISTICS, ACTION, LOCATION, (val) => val > 0);

    const checkpoints = await projectCore.getCheckpoints(BATCH_CODE);
    expect(checkpoints.length).to.equal(2);
  });

  // ================= CA KIEM THU 3: GIAN LAN / KHONG PHAN QUYEN (FRAUD CASE) =================
  it("TC-03 (Gian lan): Dia chi la khong co quyen co tinh them chang bi revert UnauthorizedCaller", async function () {
    await projectCore.connect(producer).createBatch(
      BATCH_CODE,
      PRODUCT_NAME,
      ORIGIN,
      INITIAL_URI
    );

    const ROLE_INSPECTOR = await projectCore.ROLE_INSPECTOR();

    await expect(
      projectCore.connect(attacker).addCheckpoint(
        BATCH_CODE,
        ROLE_INSPECTOR,
        "Co so gia mao khong phep",
        "Gia mao chung nhan kiem dinh OCOP Hue",
        "ipfs://QmFakeCertificateHash"
      )
    ).to.be.revertedWithCustomError(projectCore, "UnauthorizedCaller")
     .withArgs(attacker.address, ROLE_INSPECTOR);
  });

  // ================= KIEM TRA VÁ LỖI 4: CHỐNG KIỂM ĐỊNH TRÙNG LẶP & THU HỒI TEM =================
  it("TC-04 (Va loi 4 do Sinh vien phat hien): Kiem dinh OCOP 2 lan bi revert BatchAlreadyVerified", async function () {
    await projectCore.connect(producer).createBatch(
      BATCH_CODE,
      PRODUCT_NAME,
      ORIGIN,
      INITIAL_URI
    );

    // 1. Inspector verify lan 1 -> Thanh cong
    await projectCore.connect(inspector).verifyBatch(
      BATCH_CODE,
      "Chung nhan OCOP 4 sao",
      "ipfs://QmCertificateHash"
    );

    // 2. Inspector co tinh verify lan 2 tren cung ma lo -> Bi revert!
    await expect(
      projectCore.connect(inspector).verifyBatch(
        BATCH_CODE,
        "Chung nhan lan 2 trung lap",
        ""
      )
    ).to.be.revertedWithCustomError(projectCore, "BatchAlreadyVerified")
     .withArgs(BATCH_CODE);

    // 3. Kiem tra thu hoi tem kiem dinh khi phat hien vi pham
    await expect(
      projectCore.connect(inspector).revokeBatchVerification(
        BATCH_CODE,
        "Phat hien bao bi rach va nhiem khuan"
      )
    ).to.emit(projectCore, "BatchVerificationRevoked");

    const batchAfterRevoke = await projectCore.getBatch(BATCH_CODE);
    expect(batchAfterRevoke.isVerified).to.be.false;
  });
});
