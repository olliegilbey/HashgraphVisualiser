pragma solidity ^0.4.18;

contract Voting {

  bytes32[] public candidateList;
  mapping (bytes32 => uint8) public votesReceived;

  uint8[] public voterBalance;

  constructor(bytes32[] candidateNames, uint8 numVoters) public {
    candidateList = candidateNames;
    for (uint8 i = 0; i < numVoters; i++) {
      voterBalance[i] = 100;
    }
  }

  function getVotesRemaining(uint8 voterId) view public returns (uint8) {
    return voterBalance[voterId];
  }

  function totalVotesFor(bytes32 candidate) view public returns (uint8) {
    assert(validCandidate(candidate));
    return votesReceived[candidate];
  }

  function vote(uint8[] votes, uint8 voterId) public {
    for (uint i = 0; i < candidateList.length; i++) {
      assert(voterBalance[voterId] >= votes[i]);
      voterBalance[voterId] -= votes[i];
      votesReceived[candidateList[i]] += votes[i];
    }
  }

  function validCandidate(bytes32 candidate) view public returns (bool) {
    for(uint i = 0; i < candidateList.length; i++) {
      if (candidateList[i] == candidate) {
        return true;
      }
    }
    return false;
  }
}
