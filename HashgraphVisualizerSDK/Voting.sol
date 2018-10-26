pragma solidity ^0.4.18;

contract Voting {

  bytes32[] public candidateList;
  mapping (bytes32 => uint) public votesReceived;

  uint[] public voterBalance;

  constructor(bytes32[] candidateNames, uint numVoters) public {
    candidateList = candidateNames;
    voterBalance = new uint[](numVoters);
    for (uint i = 0; i < numVoters; i++) {
      voterBalance[i] = 100;
    }
  }

  function getVotesRemaining(uint voterId) view public returns (uint) {
    return voterBalance[voterId];
  }

  function totalVotesFor(bytes32 candidate) view public returns (uint) {
    assert(validCandidate(candidate));
    return votesReceived[candidate];
  }

  function vote(uint[] votes, uint voterId) public {
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
