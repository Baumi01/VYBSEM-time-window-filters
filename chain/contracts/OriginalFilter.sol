// SPDX-License-Identifier: MIT
// version 0.8.0
pragma solidity ^0.8.0;

// class that will live on the blockchain
contract OriginalFilter {
    // dictionary of revoked pseudonyms (32 byte value)
    mapping(bytes32 => bool) revoked;

    // can be called by anyone to insert a pseudonym into the dictionary
    function insert(bytes32 pseudonym) public {
        revoked[pseudonym] = true;
    }

    // can be called by anyone to remove a pseudonym from the dictionary
    function remove(bytes32 pseudonym) public {
        revoked[pseudonym] = false;
    }

    // can be called by anyone to check if a pseudonym is revoked
    function isRevoked(bytes32 pseudonym) public view returns (bool) {
        return revoked[pseudonym];
    }
}