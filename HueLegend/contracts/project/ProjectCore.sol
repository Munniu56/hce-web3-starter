// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ProjectCore (HueLegend Traceability Core)
 * @dev Hop dong thong minh truy xuat nguon goc dac san Hue tren Blockchain.
 * Quan ly lo hang, phan quyen cac vai tro trong chuoi cung ung va ghi nhan lich su bat bien.
 */
contract ProjectCore is Ownable {
    // Dinh nghia cac vai tro trong he thong truy xuat nguon goc
    bytes32 public constant ROLE_ADMIN = keccak256("ROLE_ADMIN");
    bytes32 public constant ROLE_PRODUCER = keccak256("ROLE_PRODUCER");       // Co so san xuat dac san Hue (Me xung, Tom chua, Tra sen...)
    bytes32 public constant ROLE_LOGISTICS = keccak256("ROLE_LOGISTICS");     // Don vi van chuyen / luu kho
    bytes32 public constant ROLE_RETAILER = keccak256("ROLE_RETAILER");       // Dai ly phan phoi / Cua hang ban le
    bytes32 public constant ROLE_INSPECTOR = keccak256("ROLE_INSPECTOR");     // Co quan kiem dinh chat luong / Ban quan ly OCOP

    // Cau truc mot chang trong lich su hanh trinh lo hang
    struct Checkpoint {
        uint256 timestamp;     // Thoi gian ghi nhan tren blockchain
        address recorder;      // Dia chi vi nguoi ghi nhan chang nay
        bytes32 role;          // Vai tro cua nguoi ghi nhan
        string location;       // Dia diem thuc hien (vd: Phu Hau, Ga Hue, Dong Ba...)
        string action;         // Hanh dong (vd: Thu hoach, Dong goi, Xuat kho, Kiem dinh...)
        string metadataURI;    // Duong dan IPFS hoac ma hash chung tu kiem dinh
    }

    // Cau truc thong tin tong quan cua lo dac san
    struct Batch {
        string batchCode;      // Ma lo hang duy nhat (vd: HL-MEXUNG-2026-001)
        string productName;    // Ten loai dac san Hue
        string origin;         // Nguon goc xuat xu nguyen lieu
        uint256 createdAt;     // Thoi diem tao lo hang
        address producer;      // Co so san xuat khoi tao
        bool isVerified;       // Trang thai da duoc kiem dinh OCOP hay chua
        bool exists;           // Co ton tai hay khong
    }

    // Bang luu tru lo hang theo ma lo
    mapping(string => Batch) private _batches;

    // Danh sach cac chang lich su theo tung ma lo hang
    mapping(string => Checkpoint[]) private _batchCheckpoints;

    // Danh sach tat ca cac ma lo hang da tao
    string[] private _allBatchCodes;

    // Bang phan quyen dia chi vi theo vai tro: account => role => isGranted
    mapping(address => mapping(bytes32 => bool)) private _roles;

    // ================= CAC LOI TUY BIEN (CUSTOM ERRORS) =================
    error BatchAlreadyExists(string batchCode);
    error BatchNotFound(string batchCode);
    error UnauthorizedCaller(address caller, bytes32 requiredRole);
    error EmptyString(string paramName);
    error InvalidAddress();

    // ================= CAC SU KIEN (EVENTS) =================
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

    event RoleAssigned(address indexed account, bytes32 indexed role);
    event RoleRevoked(address indexed account, bytes32 indexed role);

    // ================= HAM KHOI TAO =================
    constructor() Ownable(msg.sender) {
        // Mac dinh nguoi trien khai hop dong giu quyen Admin va Producer ban dau
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
    /**
     * @dev Cap quyen vai tro cho mot dia chi vi (Chi chu so huu / Admin moi co quyen)
     */
    function grantRole(address account, bytes32 role) external onlyOwner {
        if (account == address(0)) revert InvalidAddress();
        _roles[account][role] = true;
        emit RoleAssigned(account, role);
    }

    /**
     * @dev Thu hoi quyen vai tro cua mot dia chi vi
     */
    function revokeRole(address account, bytes32 role) external onlyOwner {
        if (account == address(0)) revert InvalidAddress();
        _roles[account][role] = false;
        emit RoleRevoked(account, role);
    }

    /**
     * @dev Kiem tra dia chi vi co nam giu vai tro cu the hay khong
     */
    function hasRole(address account, bytes32 role) external view returns (bool) {
        if (account == owner()) return true;
        return _roles[account][role];
    }

    // ================= LUONG NGHIEP VU COT LOI =================
    /**
     * @dev 1. Tao lo hang dac san moi (Chi co so san xuat moi duoc tao)
     * Ap dung mo hinh Checks-Effects-Interactions
     */
    function createBatch(
        string calldata batchCode,
        string calldata productName,
        string calldata origin,
        string calldata initialMetadataURI
    ) external onlyRole(ROLE_PRODUCER) {
        // Checks
        if (bytes(batchCode).length == 0) revert EmptyString("batchCode");
        if (bytes(productName).length == 0) revert EmptyString("productName");
        if (bytes(origin).length == 0) revert EmptyString("origin");
        if (_batches[batchCode].exists) revert BatchAlreadyExists(batchCode);

        // Effects
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

        // Tu dong ghi nhan chang dau tien: Khoi tao lo dac san tai co so
        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: ROLE_PRODUCER,
            location: origin,
            action: "Khoi tao lo hang dac san tai co so san xuat",
            metadataURI: initialMetadataURI
        }));

        // Interactions (Phat su kien thay doi trang thai)
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
     * @dev 2. Them chang hanh trinh boi dung vai tro
     * Dia chi goi ham phai duoc cap dung vai tro `role` truyen vao
     */
    function addCheckpoint(
        string calldata batchCode,
        bytes32 role,
        string calldata location,
        string calldata action,
        string calldata metadataURI
    ) external {
        // Checks
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        if (!_roles[msg.sender][role] && msg.sender != owner()) {
            revert UnauthorizedCaller(msg.sender, role);
        }
        if (bytes(location).length == 0) revert EmptyString("location");
        if (bytes(action).length == 0) revert EmptyString("action");

        // Effects
        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: role,
            location: location,
            action: action,
            metadataURI: metadataURI
        }));

        // Interactions
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
     * @dev Kiem dinh lo hang boi co quan giam dinh / OCOP
     */
    function verifyBatch(
        string calldata batchCode,
        string calldata inspectorNote,
        string calldata certificateURI
    ) external onlyRole(ROLE_INSPECTOR) {
        // Checks
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);

        // Effects
        _batches[batchCode].isVerified = true;

        _batchCheckpoints[batchCode].push(Checkpoint({
            timestamp: block.timestamp,
            recorder: msg.sender,
            role: ROLE_INSPECTOR,
            location: "Trung tam Kiem dinh OCOP Thua Thien Hue",
            action: bytes(inspectorNote).length > 0 ? inspectorNote : "Kiem dinh va chung nhan dac san Hue dat chuan",
            metadataURI: certificateURI
        }));

        // Interactions
        emit BatchVerified(batchCode, msg.sender, block.timestamp);
        emit CheckpointAdded(
            batchCode,
            msg.sender,
            ROLE_INSPECTOR,
            "Kiem dinh va chung nhan dac san Hue dat chuan",
            "Trung tam Kiem dinh OCOP Thua Thien Hue",
            block.timestamp
        );
    }

    // ================= 3. TRUY VAN XEM LICH SU (QUET QR) =================
    /**
     * @dev Lay thong tin tong quan cua lo hang theo ma lo
     */
    function getBatch(string calldata batchCode) external view returns (Batch memory) {
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        return _batches[batchCode];
    }

    /**
     * @dev Lay toan bo danh sach cac chang lich su cua lo hang de hien thi timeline
     */
    function getCheckpoints(string calldata batchCode) external view returns (Checkpoint[] memory) {
        if (!_batches[batchCode].exists) revert BatchNotFound(batchCode);
        return _batchCheckpoints[batchCode];
    }

    /**
     * @dev Lay tong so luong lo hang da khoi tao trong he thong
     */
    function getTotalBatches() external view returns (uint256) {
        return _allBatchCodes.length;
    }

    /**
     * @dev Lay ma lo hang theo chi muc (index)
     */
    function getBatchCodeByIndex(uint256 index) external view returns (string memory) {
        return _allBatchCodes[index];
    }
}
