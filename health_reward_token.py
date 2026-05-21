# v0.2.17
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
from genlayer import *


class HealthRewardToken(gl.Contract):
    """
    AI-powered reward token contract.

    Users can:
    - Transfer tokens normally
    - Submit health/activity proofs
    - Earn rewards after LLM validation

    Supported activities:
    - walking
    - running
    - cycling
    - swimming
    - gym
    - yoga
    - hiking
    - dancing
    - meditation
    etc
    """

    balances: TreeMap[Address, u256]

    # Prevent duplicate reward claims
    rewarded_activity_ids: TreeMap[str, bool]

    # Stores all rewarded activity names
    activity_names: DynArray[str]

    def __init__(self, total_supply: int) -> None:
        self.balances[gl.message.sender_address] = u256(total_supply)

    # ERC20-LIKE TRANSFER
    @gl.public.write
    def transfer(self, amount: int, to_address: str) -> None:

        sender = gl.message.sender_address
        recipient = Address(to_address)

        sender_balance = self.balances.get(sender, 0)

        if sender_balance < amount:
            raise gl.vm.UserError("Insufficient balance")

        self.balances[sender] = sender_balance - amount

        self.balances[recipient] = self.balances.get(recipient, 0) + amount

    
    # AI HEALTH / FITNESS REWARD ENGINE
    @gl.public.write
    def submit_activity(
        self,
        user_address: str,
        activity_name: str,
        activity_data: str,
        activity_id: str,
    ) -> None:
        """
        Method updated to let the AI determine the reward amount and mint tokens.
        """

        # Prevent duplicate claims 
        if self.rewarded_activity_ids.get(activity_id, False):
            raise gl.vm.UserError("Activity already rewarded")

        # Construct prompt instructing the AI to determine the reward 
        prompt_input = f"""
    You are an AI fitness and wellness validator.

    Analyze this user activity and determine an appropriate token reward (0-1000 tokens).

    Activity name:
    {activity_name}

    Activity data:
    {activity_data}

    Validation & Reward Requirements:
    - Detect fake or impossible data (0 reward if suspicious)
    - Reward healthy activities proportional to intensity and duration
    - Ensure values are physically realistic
    """

        # Update task to include reward_amount in the JSON response 
        task = """
    Return ONLY valid JSON in this exact format:

    {
        "approved": bool,
        "confidence": int,
        "health_score": int,
        "reward_amount": int,
        "reason": str
    }

    Rules:
    - confidence must be between 0 and 100
    - health_score must be between 0 and 100
    - reward_amount must be between 0 and 1000
    - approved must only be true for healthy legitimate activity
    - reason should be atleast 200 characters
    - output ONLY JSON
    """

        criteria = """
    Healthy realistic activities should be rewarded.
    The reward_amount should reflect the physical effort described in activity_data.
    Impossible or fraudulent activities should be rejected with 0 reward.
    The evaluation must be medically and physically reasonable.
    """

        # Use non-comparative equivalence principle for subjective evaluation 
        llm_result = (
            gl.eq_principle.prompt_non_comparative(
                lambda: prompt_input,
                task=task,
                criteria=criteria,
            )
            .replace("```json", "")
            .replace("```", "")
        )

        result_json = json.loads(llm_result)

        approved = result_json["approved"]
        confidence = result_json["confidence"]
        # AI-determined reward 
        reward_amount = result_json["reward_amount"]

        if not approved:
            raise gl.vm.UserError(result_json["reason"])

        if confidence < 70:
            raise gl.vm.UserError("Low confidence validation")

        recipient = Address(user_address)

        # "Mint" new tokens to the user 
        # By directly increasing the recipient's balance without deducting from a treasury,
        # the contract effectively creates/mints these tokens in its local state.
        current_balance = self.balances.get(recipient, 0)
        self.balances[recipient] = current_balance + u256(reward_amount)

        # Store activity name in DynArray
        self.activity_names.append(activity_name)

        # Mark claim as used in TreeMap 
        self.rewarded_activity_ids[activity_id] = True
        # Return the AI's output directly to the caller 
        return llm_result


    
    # VIEWS
    @gl.public.view
    def get_balance_of(self, address: str) -> int:
        return self.balances.get(Address(address), 0)

    @gl.public.view
    def get_balances(self) -> dict[str, int]:
        return {k.as_hex: v for k, v in self.balances.items()}

    @gl.public.view
    def is_activity_rewarded(self, activity_id: str) -> bool:
        return self.rewarded_activity_ids.get(activity_id, False)

    @gl.public.view
    def get_activity_names(self) -> list[str]:
        return [name for name in self.activity_names]
