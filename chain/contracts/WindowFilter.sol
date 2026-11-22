// SPDX-License-Identifier: MIT
// version 0.8.0
pragma solidity ^0.8.0;

// proposed design - filter for each time window
contract WindowFilter {
    // dictionary of revoked pseudonyms for each time window
    mapping(uint256 => mapping(bytes32 => bool)) revoked;

    // dictionary of discarded time windows
    mapping(uint256 => bool) discarded;

    // add a pseudonym to the revoked list for a specific time window
    function insert(uint256 window, bytes32 pseudonym) public {
        revoked[window][pseudonym] = true;
    }

    // costs only one transaction to remove a whole filter bound to a time window
    function discardWindow(uint256 window) public {
        discarded[window] = true;
    }

    // check if revoked; revoked only when the time window is not discarded and the pseudonym is in the revoked list
    function isRevoked(uint256 window, bytes32 pseudonym) public view returns (bool) {
        if (discarded[window]) {
            return false;
        } else {
            return revoked[window][pseudonym];
        }
    }
}