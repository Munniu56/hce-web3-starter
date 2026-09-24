// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

/// @title Hello World Smart Contract
/// @author Dr. Long Ha
contract HelloWorld {
    string private s_greeting;
    uint256 public s_updateCount;

    event GreetingChanged(
        address indexed updater,
        string oldGreeting,
        string newGreeting,
        uint256 timestamp
    );

    constructor(string memory _initialGreeting) {
        s_greeting = _initialGreeting;
        s_updateCount = 0;
    }

    function setGreeting(string calldata _newGreeting) external {
        string memory oldGreeting = s_greeting;
        s_greeting = _newGreeting;
        unchecked {
            ++s_updateCount;
        }
        emit GreetingChanged(msg.sender, oldGreeting, _newGreeting, block.timestamp);
    }

    function getGreeting() external view returns (string memory) {
        return s_greeting;
    }
}