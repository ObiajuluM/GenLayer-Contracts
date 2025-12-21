# { "Depends": "py-genlayer:latest" }
from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class Voter:
    weight: u256
    voted: bool
    vote: u256


@allow_storage
@dataclass
class Proposal:
    name: str
    vote_count: u256


class Voting(gl.Contract):
    chairperson: Address
    # Storage for voters: maps address to Voter struct
    voters: TreeMap[Address, Voter]
    # Storage for iterating voters: maps index to address
    voter_indices: TreeMap[u256, Address]
    # Storage for proposals: maps index to Proposal struct
    proposals: TreeMap[u256, Proposal]
    # Counters for voters and proposals
    voter_count: u256
    proposal_count: u256

    @gl.public.write
    def add_proposal(self, proposal_name: str):
        # Only the chairperson can add new proposals
        assert (
            gl.message.sender_address == self.chairperson
        ), "Only chairperson can add proposals."
        # Create a new proposal and add it to the map
        self.proposals[self.proposal_count] = Proposal(proposal_name, 0)
        self.proposal_count += 1

    @gl.public.view
    def all_proposals(self) -> dict:
        # Return all proposals as a dictionary for easy frontend consumption
        proposals = {}
        for i in range(self.proposal_count):
            p = self.proposals[i]
            proposals[str(i)] = {"name": p.name, "vote_count": p.vote_count}
        return proposals

    @gl.public.view
    def all_voters(self) -> dict:
        # Return all voters as a dictionary by iterating through indices
        voters = {}
        for i in range(self.voter_count):
            voter_address = self.voter_indices[i]
            voter = self.voters[voter_address]
            voters[str(i)] = {
                "address": str(voter_address),
                "weight": voter.weight,
                "voted": voter.voted,
                "vote": voter.vote,
            }
        return voters

    @gl.public.view
    def get_proposal(self, proposal_id: int) -> dict:
        # Get a single proposal by ID
        proposal = self.proposals[proposal_id]
        return {"name": proposal.name, "vote_count": proposal.vote_count}

    @gl.public.view
    def get_voter(self, voter: str) -> dict:
        # Get a single voter's details by address
        voter = Address(voter)
        v = self.voters.get(voter, Voter(0, False, 0))
        return {
            "address": str(voter),
            "weight": v.weight,
            "voted": v.voted,
            "vote": v.vote,
        }

    @gl.public.view
    def total_proposals(self) -> int:
        # Return total number of proposals
        return self.proposal_count

    @gl.public.view
    def total_voters(self) -> int:
        # Return total number of registered voters
        return self.voter_count

    def __init__(self, _initial_proposal_name: str):
        # Initialize the contract with one proposal
        self.chairperson = gl.message.sender_address
        self.voter_count = 0
        self.proposals[self.proposal_count] = Proposal(_initial_proposal_name, 0)
        self.proposal_count += 1

    @gl.public.write
    def give_right_to_vote(self, voter: str):
        # Give a voter the right to vote (only chairperson)
        assert (
            gl.message.sender_address == self.chairperson
        ), "Only chairperson can give right to vote."
        assert not self.voters.get(
            voter, Voter(0, False, 0)
        ).voted, "You can't get permission if you already used your vote."

        assert (
            self.voters.get(voter, Voter(0, False, 0)).weight == 0
        ), "If they already have weight, they are already registered."

        voter = Address(voter)
        # Initialize voter with weight 1
        self.voters[voter] = Voter(1, False, 0)
        # Add to indices for iteration
        self.voter_indices[self.voter_count] = voter
        self.voter_count += 1

    @gl.public.write
    def vote(self, proposal: int):
        # Cast a vote for a proposal
        assert not self.voters[gl.message.sender_address].voted
        assert proposal < self.proposal_count

        # Record the vote
        self.voters[gl.message.sender_address].vote = proposal
        self.voters[gl.message.sender_address].voted = True
        # Add weight to the proposal
        self.proposals[proposal].vote_count += self.voters[
            gl.message.sender_address
        ].weight
        # Reset weight to prevent double voting (though voted flag handles this too)
        self.voters[gl.message.sender_address].weight = 0

    def _winning_proposal(self) -> int:
        # Internal function to calculate the winning proposal
        # Start assuming the highest score is 0.
        winning_vote_count: u256 = 0
        # Start assuming proposal #0 is the winner.
        winning_proposal: u256 = 0
        # Loop through all proposals.
        for i in range(len(self.proposals)):
            # If the current proposal has more votes than our current winner...
            if self.proposals[i].vote_count > winning_vote_count:
                # ...update the highest score.
                winning_vote_count = self.proposals[i].vote_count
                # ...update the winner ID.
                winning_proposal = i
        # Return the ID of the winner.
        return winning_proposal

    @gl.public.view
    def winning_proposal(self) -> int:
        # Public way to ask "Who won?" (returns the ID).
        return self._winning_proposal()

    @gl.public.view
    def winner_name(self) -> str:
        # Find the winner ID, look up the name in the list, and return the name.
        return self.proposals[self._winning_proposal()].name
