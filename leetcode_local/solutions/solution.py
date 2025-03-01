def two_sum(nums, target):
    """
    Given an array of integers nums and an integer target, 
    return indices of the two numbers such that they add up to target.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # Create a dictionary to store value -> index mapping
    num_map = {}
    
    # Iterate through the array
    for i, num in enumerate(nums):
        # Calculate the complement (the number we need to find)
        complement = target - num
        
        # Check if the complement exists in our map
        if complement in num_map:
            # Return the indices of the two numbers
            return [num_map[complement], i]
        
        # Add the current number to our map
        num_map[num] = i
    
    # No solution found (though the problem guarantees one exists)
    return []


# Test your solution
if __name__ == "__main__":
    # Example test cases
    print(two_sum(nums=[2, 7, 11, 15], target=9))  # Expected: [0, 1]
    print(two_sum(nums=[3, 2, 4], target=6))       # Expected: [1, 2]
    print(two_sum(nums=[3, 3], target=6))          # Expected: [0, 1]