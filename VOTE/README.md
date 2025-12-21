# Voting Contract

This is a decentralized voting contract implemented in Python using the `genlayer` framework. It allows a chairperson to create proposals and register voters, who can then cast their votes for their preferred proposals.

## Features

- **Chairperson Control**: A designated chairperson (the contract deployer) manages the voting process.
- **Voter Registration**: The chairperson gives rights to vote to specific addresses.
- **Proposal Management**: The chairperson can add multiple proposals.
- **Voting**: Registered voters can cast one vote for a proposal.
- **Transparency**: Anyone can view all proposals, voters, and the current state of the vote.
- **Result Calculation**: The contract automatically calculates the winning proposal based on vote counts.

## Contract Structure

### Data Structures

- **`Voter`**: Stores voter information.
    - `weight` (u256): Weight of the vote (usually 1).
    - `voted` (bool): Whether the voter has already voted.
    - `vote` (u256): Index of the proposal voted for.

- **`Proposal`**: Stores proposal information.
    - `name` (str): Name of the proposal.
    - `vote_count` (u256): Number of votes received.

### State Variables

- `chairperson`: Address of the contract creator.
- `voters`: Mapping of addresses to `Voter` objects.
- `voter_indices`: Mapping of indices to voter addresses (for iteration).
- `proposals`: Mapping of indices to `Proposal` objects.
- `voter_count`: Total number of registered voters.
- `proposal_count`: Total number of proposals.

## Methods

### Write Methods (Transactions)

- **`__init__(self, _initial_proposal_name: str)`**: 
  Initializes the contract, sets the sender as chairperson, and creates the first proposal.

- **`add_proposal(self, proposal_name: str)`**: 
  Allows the chairperson to add a new proposal.

- **`give_right_to_vote(self, voter: str)`**: 
  Allows the chairperson to register a new voter. The voter must not have voted or be already registered.

- **`vote(self, proposal: int)`**: 
  Allows a registered voter to cast their vote for a specific proposal ID.

### View Methods (Read-Only)

- **`all_proposals(self) -> dict`**: 
  Returns a dictionary of all proposals.

- **`all_voters(self) -> dict`**: 
  Returns a dictionary of all registered voters.

- **`get_proposal(self, proposal_id: int) -> dict`**: 
  Returns details of a specific proposal.

- **`get_voter(self, voter: str) -> dict`**: 
  Returns details of a specific voter.

- **`total_proposals(self) -> int`**: 
  Returns the total count of proposals.

- **`total_voters(self) -> int`**: 
  Returns the total count of voters.

- **`winning_proposal(self) -> int`**: 
  Returns the index of the proposal with the most votes.

- **`winner_name(self) -> str`**: 
  Returns the name of the winning proposal.

## Usage Workflow

1.  **Deploy**: The contract is deployed with an initial proposal name. The deployer becomes the chairperson.
2.  **Add Proposals**: The chairperson calls `add_proposal` to add more options.
3.  **Register Voters**: The chairperson calls `give_right_to_vote` for each eligible voter address.
4.  **Vote**: Registered voters call `vote` with the index of their chosen proposal.
5.  **Tally**: Anyone can call `winning_proposal` or `winner_name` to see the results.

## Future Improvements

- **Vote Delegation**: Support for delegating votes to other voters is coming soon.

## Dependencies

- `py-genlayer:latest`
