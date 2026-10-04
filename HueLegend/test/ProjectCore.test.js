const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("HueLegend - ProjectCore (Traceability Test Suite)", function () {
  let projectCore;
  let owner, producer, logistics, retailer, inspector, attacker;

  const BATCH_CODE = "HL-MEXUNG-2026-001";
  const PRODUCT_NAME = "Me Xung Thien Huong Thuong Hang";
  const ORIGIN = "Phu Hau, TP Hue";
  const INITIAL_URI = "ipfs://QmHueMeXungOCOP4StarBatch001";

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
  });

  // ================= CA KIEM THU 1: HOP LE (CREATION) =================
  it("TC-01: Co so san xuat tao lo hang dac san thanh cong va phat event", async function () {
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

    // Kiem tra chang khoi tao dau tien da duoc tu dong luu
    const checkpoints = await projectCore.getCheckpoints(BATCH_CODE);
    expect(checkpoints.length).to.equal(1);
    expect(checkpoints[0].location).to.equal(ORIGIN);
    expect(checkpoints[0].recorder).to.equal(producer.address);
  });

  // ================= CA KIEM THU 2: HOP LE (CHECKPOINT BY ROLE) =================
  it("TC-02: Don vi van chuyen (dung vai tro) them chang hanh trinh thanh cong", async function () {
    // 1. Co so tao lo hang truoc
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

    // 2. Logistics them chang dung vai
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
    expect(checkpoints[1].location).to.equal(LOCATION);
    expect(checkpoints[1].action).to.equal(ACTION);
    expect(checkpoints[1].recorder).to.equal(logistics.address);
  });

  // ================= CA KIEM THU 3: GIAN LAN / KHONG PHAN QUYEN (FRAUD CASE) =================
  it("TC-03 (Gian lan): Dia chi la khong co quyen co tinh them chang bi revert UnauthorizedCaller", async function () {
    // 1. Co so san xuat tao lo hang
    await projectCore.connect(producer).createBatch(
      BATCH_CODE,
      PRODUCT_NAME,
      ORIGIN,
      INITIAL_URI
    );

    const ROLE_INSPECTOR = await projectCore.ROLE_INSPECTOR();

    // 2. Attacker (ke xau) gia mao lam Inspector de chung nhan khong dung su that
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

    // Kiem tra so luong chang khong bi thay doi hay bi chen du lieu gia
    const checkpoints = await projectCore.getCheckpoints(BATCH_CODE);
    expect(checkpoints.length).to.equal(1);
  });

  // ================= CA KIEM THU 4: RANG BUOC MA LO KHONG TRUNG LAP =================
  it("TC-04: Khong cho phep tao trung ma lo hang (BatchAlreadyExists)", async function () {
    await projectCore.connect(producer).createBatch(
      BATCH_CODE,
      PRODUCT_NAME,
      ORIGIN,
      INITIAL_URI
    );

    await expect(
      projectCore.connect(producer).createBatch(
        BATCH_CODE,
        "Me Xung Loai 2",
        "Dia chi khac",
        ""
      )
    ).to.be.revertedWithCustomError(projectCore, "BatchAlreadyExists")
     .withArgs(BATCH_CODE);
  });
});
