# Example Run — DocForge Pipeline

## Input

A simple ERC-20 token contract with staking functionality:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract StakingToken is ERC20, Ownable {
    uint256 public rewardRate = 100; // basis points per year
    mapping(address => uint256) public stakedBalance;
    mapping(address => uint256) public lastStakeTime;
    uint256 public totalStaked;
    
    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 reward);
    
    constructor() ERC20("StakingToken", "STK") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10**18);
    }
    
    function stake(uint256 amount) external {
        require(amount > 0, "Cannot stake 0");
        _transfer(msg.sender, address(this), amount);
        stakedBalance[msg.sender] += amount;
        lastStakeTime[msg.sender] = block.timestamp;
        totalStaked += amount;
        emit Staked(msg.sender, amount);
    }
    
    function withdraw(uint256 amount) external {
        require(stakedBalance[msg.sender] >= amount, "Insufficient staked balance");
        stakedBalance[msg.sender] -= amount;
        totalStaked -= amount;
        _transfer(address(this), msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }
    
    function claimReward() external {
        uint256 reward = calculateReward(msg.sender);
        require(reward > 0, "No reward");
        lastStakeTime[msg.sender] = block.timestamp;
        _mint(msg.sender, reward);
        emit RewardClaimed(msg.sender, reward);
    }
    
    function calculateReward(address user) public view returns (uint256) {
        if (stakedBalance[user] == 0) return 0;
        uint256 duration = block.timestamp - lastStakeTime[user];
        return (stakedBalance[user] * rewardRate * duration) / (365 days * 10000);
    }
    
    function setRewardRate(uint256 newRate) external onlyOwner {
        require(newRate <= 1000, "Rate too high");
        rewardRate = newRate;
    }
}
```

## Pipeline Execution

### Step 1: Upload
```
POST /document
→ {"id": "f8a2b3c4d5e6", "status": "queued", "filename": "StakingToken.sol"}
```

### Step 2: Parallel Agent Execution (~8-12 seconds)

All 5 agents run concurrently:

| Agent | Status | Tokens | Latency |
|-------|--------|--------|---------|
| API Documenter | ✅ | 3,240 | 2.1s |
| Architecture Analyzer | ✅ | 2,890 | 1.9s |
| Security Note Generator | ✅ | 3,560 | 2.4s |
| Usage Example Generator | ✅ | 4,120 | 3.1s |
| Changelog Generator | ✅ | 2,340 | 1.6s |

### Step 3: Synthesis (~4-6 seconds)

| Agent | Status | Tokens | Latency |
|-------|--------|--------|---------|
| Synthesis | ✅ | 7,850 | 4.8s |

### Step 4: Result

Total pipeline: ~12 seconds, ~24,000 tokens

### Token Stats
```json
{
  "total_calls": 6,
  "total_tokens": 24000,
  "by_agent": {
    "api_documenter": {"calls": 1, "total_tokens": 3240, "avg_latency_ms": 2100},
    "architecture_analyzer": {"calls": 1, "total_tokens": 2890, "avg_latency_ms": 1900},
    "security_note_generator": {"calls": 1, "total_tokens": 3560, "avg_latency_ms": 2400},
    "usage_example_generator": {"calls": 1, "total_tokens": 4120, "avg_latency_ms": 3100},
    "changelog_generator": {"calls": 1, "total_tokens": 2340, "avg_latency_ms": 1600},
    "synthesis": {"calls": 1, "total_tokens": 7850, "avg_latency_ms": 4800}
  }
}
```

## Output Preview

The generated documentation includes:
- **Overview**: ERC-20 staking token with time-based rewards
- **Architecture**: Mermaid class diagram showing ERC20 + Ownable inheritance
- **API Reference**: 6 functions fully documented with NatSpec
- **Security Notes**: Reentrancy risk on `withdraw()`, centralization risk on `setRewardRate()`, 6/10 risk score
- **Usage Guide**: Hardhat deployment script, ethers.js examples, test skeleton
- **Changelog**: v1.0.0 initial release entry
