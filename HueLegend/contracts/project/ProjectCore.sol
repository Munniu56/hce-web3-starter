// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ProjectCore (HueLegend Traceability & Escrow Core - Post-Audit Version)
 * @dev Hop dong thong minh truy xuat nguon goc dac san Hue da qua kiem toan Lab 10.
 * Khac phuc 4 loi nghiem trong: Rang buoc tien coc, Logic gia han khoa coc, Gioi han chang DoS va Chuyen biet hoa quy trinh kiem dinh OCOP.
 */
contract ProjectCore is Ownable {
    // ================= 1. DINH NGHIA VAI TRO (RBAC) =================
    bytes32 public constant ROLE_ADMIN = keccak256("ROLE_ADMIN");
    bytes32 public constant ROLE_PRODUCER = keccak256("ROLE_PRODUCER");       // Co so san xuat dac san Hue (Me xung, Tom chua, Tra sen...)
    bytes32 public constant ROLE_LOGISTICS = keccak256("ROLE_LOGISTICS");     // Don vi van chuyen / luu kho
    bytes32 public constant ROLE_RETAILER = keccak256("ROLE_RETAILER");       // Dai ly phan phoi / Cua hang ban le
    bytes32 public constant ROLE_INSPECTOR = keccak256("ROLE_INSPECTOR");     // Co quan kiem dinh chat luong OCOP

    // Tham so ky quy bao dam va gioi han chong DoS
    uint256 public constant MIN_STAKE_AMOUNT = 0.05 ether;
    uint256 public constant MAX_CHECKPOINTS_PER_BATCH = 50; // Khac phuc loi DoS mang dong
    uint256 public stakeLockDuration = 30 days;            // Thoi gian khoa coc mac dinh

    // ================= 2. CAU TRUC DU LIEU (STRUCTS) =================
    struct Checkpoint {
        uint256 timestamp;     // Thoi gian ghi nhan tren blockchain
        address recorder;      // Dia chi vi nguoi ghi nhan chang nay
        bytes32 role;          // Vai tro cua nguoi ghi nhan
        string location;       // Dia diem thuc hien (vd: Phu Hau, Ga Hue, Dong Ba...)
        string action;         // Hanh dong (vd: Thu hoach, Dong goi, Xuat kho, Kiem dinh...)
        string metadataURI;    // Duong dan IPFS hoac ma hash chung tu kiem dinh
    }

    struct Batch {
        string batchCode;      // Ma lo hang duy nhat (vd: HL-MEXUNG-2026-001)
        string productName;    // Ten loai dac san Hue
        string origin;         // Nguon goc xuat xu nguyen lieu
        uint256 createdAt;     // Thoi diem tao lo hang
        address producer;      // Co so san xuat khoi tao
        bool isVerified;       // Trang thai da duoc kiem dinh OCOP hay chua
        bool exists;           // Co ton tai hay khong
    }

    // ================= 3. BANG LUU TRU TRANG THAI =================
    mapping(string => Batch) private _batches;
    mapping(string => Checkpoint[]) private _batchCheckpoints;
    string[] private _allBatchCodes;

    mapping(address => mapping(bytes32 => bool)) private _roles;

    // Quan ly tien ky quy va thoi gian mo khoa cua tung co so san xuat
    mapping(address => uint256) public producerStake;
    mapping(address => uint256) public producerUnlockTime;

    // ================= 4. CAC LOI TUY BIEN (CUSTOM ERRORS) =================
    error BatchAlreadyExists(string batchCode);
    error BatchNotFound(string batchCode);
    error UnauthorizedCaller(address caller, bytes32 requiredRole);
    error EmptyString(string paramName);
    error InvalidAddress();
    error ZeroAmount();
    error StillLocked(uint256 unlockAt, uint256 currentTime);
    error NothingToWithdraw();
    error TransferFailed();
    error StakeTooLow(uint256 provided, uint256 minimum);
    error MaxCheckpointsExceeded(string batchCode, uint256 maxAllowed); // Loi 3 khac phuc DoS
    error BatchAlreadyVerified(string batchCode);                      // Loi 4 kiem dinh trung lap
    error BatchNotVerified(string batchCode);                          // Loi 4 thu hoi khi chua verify

    // ================= 5. CAC SU KIEN (EVENTS) =================
    event BatchCreated(
        string indexed batchCode,
        string productName,
        address indexed producer,
        uint256 timestamp
    );

    event CheckpointAdded(
        string indexed batchCode,
        address indexed recorder,
        bytes32 indexed role,
        string action,
        string location,
        uint256 timestamp
    );

    event BatchVerified(
        string indexed batchCode,
        address indexed inspector,
        uint256 timestamp
    );

    event BatchVerificationRevoked(
        string indexed batchCode,
        address indexed inspector,
        string reason,
        uint256 timestamp
    );

    event RoleAssigned(address indexed account, bytes32 indexed role);
    event RoleRevoked(address indexed account, bytes32 indexed role);

    event StakeDeposited(address indexed producer, uint256 amount, uint256 unlockTime);
    event StakeWithdrawn(address indexed producer, uint256 amount);
    event StakeLockDurationUpdated(uint256 oldDuration, uint256 newDuration);

    // ================= HAM KHOI TAO =================
    constructor() Ownable(msg.sender) {
        _roles[msg.sender][ROLE_ADMIN] = true;
        _roles[msg.sender][ROLE_PRODUCER] = true;

        emit RoleAssigned(msg.sender, ROLE_ADMIN);
        emit RoleAssigned(msg.sender, ROLE_PRODUCER);
    }

    // ================= MODIFIERS KIEM TRA QUYEN =================
    modifier onlyRole(bytes32 role) {
        if (!_roles[msg.sender][role] && msg.sender != owner()) {
            revert UnauthorizedCaller(msg.sender, role);
        }
        _;
    }

    // ================= QUAN LY PHAN QUYEN =================
    function grantRole(address account, bytes32 role) external onlyOwner {
        if (account == address(0)) revert InvalidAddress();
        _roles[account][role] = true;
        emit RoleAssigned(account, role);
    }

    function revokeRole(address account, bytes32 role) external onlyOwner {
        if (account == address(0)) revert InvalidAddress();
        _roles[account][role] = false;
        emit RoleRevoked(account, role);
    }

    function hasRole(address account, bytes32 role) external view returns (bool) {
        if (account == owner()) return true;
        return _roles[account][role];
    }

    function setStakeLockDuration(uint256 newDuration) external onlyOwner {
        uint256 old = stakeLockDuration;
        stakeLockDuration = newDuration;
        emit StakeLockDurationUpdated(old, newDuration);
    }

    // ================= KY GUI CO KHOA THOI GIAN (TIMELOCK STAKING) =================
    /**
     * @dev Nap tien ky quy cam ket chat luong.
     * Khac phuc Loi 2 (Audit): Khong reset oan thoi gian khoa neu da nap cọc tu truoc va chua het han
     */
    function depositStake() external payable {
        if (msg.value == 0) revert ZeroAmount();

        producerStake[msg.sender] += msg.value;

        // Chi cap nhat unlockTime moi neu chua tung khoa hoac da qua thoi gian khoa cu
        if (block.timestamp >= producerUnlockTime[msg.sender]) {
            uint256 unlockAt = block.timestamp + stakeLockDuration;
            producerUnlockTime[msg.sender] = unlockAt;
            emit StakeDeposited(msg.sender, msg.value, unlockAt);
        } else {
            // Giu nguyen mốc mở khóa cũ, bảo vệ quyền lợi người nạp bổ sung
            emit StakeDeposited(msg.sender, msg.value, producerUnlockTime[msg.sender]);
        }
    }

    /**
     * @dev Rut tien ky quy sau khi het thoi gian khoa theo mo hinh Checks-Effects-Interactions
     */
    function withdrawStake() external {
        // 1. Checks
        uint256 amount = producerStake[msg.sender];
        if (amount == 0) revert NothingToWithdraw();

        uint256 unlockAt = producerUnlockTime[msg.sender];
        if (block.timestamp < unlockAt) {
            revert StillLocked(unlockAt, block.timestamp);
        }

        // 2. Effects
        producerStake[msg.sender] = 0;
        emit StakeWithdrawn(msg.sender, amount);

        // 3. Interactions
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        if (!ok) revert TransferFailed();
    }

    function getStakeInfo(address producer) external view returns (
        uint256 balance,
        uint256 unlockAt,
        uint256 remainingSeconds
    ) {
        balance = producerStake[producer];
        unlockAt = producerUnlockTime[producer];
        if (block.timestamp >= unlockAt) {
            remainingSeconds = 0;
        } else {
            remainingSeconds = unlockAt - block.timestamp;
        }
    }

    // ================= LUONG TRUY XUAT NGUON GOC COT LOI =================
    /**
     * @dev 1. Tao lo hang dac san moi.
     * Khac phuc Loi 1 (Audit): Bat buoc co so phai co du tien ky quy MIN_STAKE_AMOUNT truoc khi tao lo
     */
    function createBatch(
        string calldata batchCode,
        string calldata productName,
        string calldata origin,
        string calldata initialMetadataURI
    ) external onlyRole(ROLE_PRODUCER) {
        // 1. Checks
        if (bytes(batchCode).length == 0) revert EmptyString("batchCode");
        if (bytes(productName).length == 0) revert EmptyString("productName");
        if (bytes(origin).length == 0) revert EmptyString("origin");
        if (_batches[batchCode].exists) revert BatchAlreadyExists(batchCode);

        // Kiem tra tien ky quy uy tin lang nghe
        if (producerStake[msg.sender] < MIN_STAKE_AMOUNT && msg.sender != owner()) {
            revert StakeTooLow(producerStake[msg.sender], MIN_STAKE_AMOUNT);
        }

        // 2. Effects
        _batches[batchCode] = Batch({
            batchCode: batchCode,
            productName: productName,
            origin: origin,
            createdAt: block.timestamp,
            producer: msg.sender,
            isVerified: false,
            exists: true
        });

        _allBatchCodes.push(batchCode);

        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: ROLE_PRODUCER,
            location: origin,
            action: "Khoi tao lo hang dac san tai co so san xuat",
            metadataURI: initialMetadataURI
        }));

        // 3. Interactions
        emit BatchCreated(batchCode, productName, msg.sender, block.timestamp);
        emit CheckpointAdded(
            batchCode,
            msg.sender,
            ROLE_PRODUCER,
            "Khoi tao lo hang dac san tai co so san xuat",
            origin,
            block.timestamp
        );
    }

    /**
     * @dev 2. Them chang hanh trinh boi dung vai tro.
     * Khac phuc Loi 3 (Audit): Gioi han toi da MAX_CHECKPOINTS_PER_BATCH de chong tan cong DoS lam tran bo nho DApp
     */
    function addCheckpoint(
        string calldata batchCode,
        bytes32 role,
        string calldata location,
        string calldata action,
        string calldata metadataURI
    ) external {
        // 1. Checks
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        if (!_roles[msg.sender][role] && msg.sender != owner()) {
            revert UnauthorizedCaller(msg.sender, role);
        }
        if (bytes(location).length == 0) revert EmptyString("location");
        if (bytes(action).length == 0) revert EmptyString("action");

        // Chong DoS tran mang dong
        if (_batchCheckpoints[batchCode].length >= MAX_CHECKPOINTS_PER_BATCH) {
            revert MaxCheckpointsExceeded(batchCode, MAX_CHECKPOINTS_PER_BATCH);
        }

        // 2. Effects
        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: role,
            location: location,
            action: action,
            metadataURI: metadataURI
        }));

        // 3. Interactions
        emit CheckpointAdded(
            batchCode,
            msg.sender,
            role,
            action,
            location,
            block.timestamp
        );
    }

    /**
     * @dev 3. Kiem dinh va chung nhan OCOP.
     * Khac phuc Loi 4 (Audit do Sinh vien phat hien): Ngan chan kiem dinh trung lap nhieu lan
     */
    function verifyBatch(
        string calldata batchCode,
        string calldata inspectorNote,
        string calldata certificateURI
    ) external onlyRole(ROLE_INSPECTOR) {
        // 1. Checks
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        if (_batches[batchCode].isVerified) revert BatchAlreadyVerified(batchCode);

        // 2. Effects
        _batches[batchCode].isVerified = true;

        string memory act = bytes(inspectorNote).length > 0 ? inspectorNote : "Kiem dinh va chung nhan dac san Hue dat chuan OCOP";

        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: ROLE_INSPECTOR,
            location: "Trung tam Kiem dinh OCOP Thua Thien Hue",
            action: act,
            metadataURI: certificateURI
        }));

        // 3. Interactions
        emit BatchVerified(batchCode, msg.sender, block.timestamp);
        emit CheckpointAdded(
            batchCode,
            msg.sender,
            ROLE_INSPECTOR,
            act,
            "Trung tam Kiem dinh OCOP Thua Thien Hue",
            block.timestamp
        );
    }

    /**
     * @dev 4. Thu hoi tem kiem dinh OCOP khi phat hien vi pham ve sinh an toan thuc pham.
     * Khac phuc Loi 4 (Bo sung nghiep vu an toan thuc pham)
     */
    function revokeBatchVerification(
        string calldata batchCode,
        string calldata reason
    ) external onlyRole(ROLE_INSPECTOR) {
        // 1. Checks
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        if (!_batches[batchCode].isVerified) revert BatchNotVerified(batchCode);
        if (bytes(reason).length == 0) revert EmptyString("reason");

        // 2. Effects
        _batches[batchCode].isVerified = false;

        string memory actionMsg = string.concat("Thu hoi chung nhan OCOP do vi pham: ", reason);

        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: ROLE_INSPECTOR,
            location: "Trung tam Kiem dinh OCOP Thua Thien Hue",
            action: actionMsg,
            metadataURI: ""
        }));

        // 3. Interactions
        emit BatchVerificationRevoked(batchCode, msg.sender, reason, block.timestamp);
        emit CheckpointAdded(
            batchCode,
            msg.sender,
            ROLE_INSPECTOR,
            actionMsg,
            "Trung tam Kiem dinh OCOP Thua Thien Hue",
            block.timestamp
        );
    }

    // ================= 5. TRUY VAN XEM LICH SU (QUET QR) =================
    function getBatch(string calldata batchCode) external view returns (Batch memory) {
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        return _batches[batchCode];
    }

    function getCheckpoints(string calldata batchCode) external view returns (Checkpoint[] memory) {
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        return _batchCheckpoints[batchCode];
    }

    function getTotalBatches() external view returns (uint256) {
        return _allBatchCodes.length;
    }

    function getBatchCodeByIndex(uint256 index) external view returns (string memory) {
        return _allBatchCodes[index];
    }
}
