# leetcode_local/problems/arrays_and_hashing.py
from . import Problem, Difficulty

TWO_SUM = Problem(
    id=1,
    title="Two Sum",
    description="""
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    You can return the answer in any order.
    """,
    examples=[
        {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
        {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]},
        {"input": {"nums": [3, 3], "target": 6}, "output": [0, 1]}
    ],
    constraints="""
    - 2 <= nums.length <= 10^4
    - -10^9 <= nums[i] <= 10^9
    - -10^9 <= target <= 10^9
    - Only one valid answer exists.
    """,
    difficulty=Difficulty.EASY,
    category="Arrays & Hashing",
    function_name="two_sum"
)

VALID_ANAGRAM = Problem(
    id=242,
    title="Valid Anagram",
    description="""
    Given two strings s and t, return true if t is an anagram of s, and false otherwise.
    An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
    typically using all the original letters exactly once.
    """,
    examples=[
        {"input": {"s": "anagram", "t": "nagaram"}, "output": True},
        {"input": {"s": "rat", "t": "car"}, "output": False}
    ],
    constraints="""
    - 1 <= s.length, t.length <= 5 * 10^4
    - s and t consist of lowercase English letters.
    """,
    difficulty=Difficulty.EASY,
    category="Arrays & Hashing",
    function_name="is_anagram"
)