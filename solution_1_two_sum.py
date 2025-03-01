# LeetCode Problem 1: Two Sum
# EASY - Arrays & Hashing

"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    You can return the answer in any order.

Examples:
  {'nums': [2, 7, 11, 15], 'target': 9} -> [0, 1]
  {'nums': [3, 2, 4], 'target': 6} -> [1, 2]
  {'nums': [3, 3], 'target': 6} -> [0, 1]

Constraints:
- 2 <= nums.length <= 10^4
    - -10^9 <= nums[i] <= 10^9
    - -10^9 <= target <= 10^9
    - Only one valid answer exists.
"""

def two_sum(nums, target):
    num_indices = {}  # Dictionary to store number and its index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_indices:
            return [num_indices[complement], i]
        num_indices[num] = i

    return []  


# Test your solution
if __name__ == "__main__":
    # Example test cases
        print(two_sum(**{'nums': [2, 7, 11, 15], 'target': 9}))  # Expected: [0, 1]
        print(two_sum(**{'nums': [3, 2, 4], 'target': 6}))  # Expected: [1, 2]
        print(two_sum(**{'nums': [3, 3], 'target': 6}))  # Expected: [0, 1]
