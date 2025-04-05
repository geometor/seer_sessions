# Code used for analysis (same as in thought process)
import numpy as np

def _find_non_zero_subsequences(digits):
    subsequences = []
    start_index = -1
    n = len(digits)
    if n == 0: return []
    for i, digit in enumerate(digits):
        if digit != 0 and start_index == -1: start_index = i
        elif (digit == 0 or i == n - 1) and start_index != -1:
            end_index = i - 1 if digit == 0 else i
            length = end_index - start_index + 1
            subsequences.append((start_index, end_index, length))
            start_index = -1
    return subsequences

def _find_longest_subsequence(subsequences):
    if not subsequences: return None
    longest_sub = subsequences[0]
    max_len = longest_sub[2]
    for sub in subsequences[1:]:
        if sub[2] > max_len:
            max_len = sub[2]
            longest_sub = sub
    return longest_sub

# Analysis Results:
# Example 1: Input=[9,9,9,0,9,9,9,9,9,0,9,9], Expected=[9,9,9,0,1,1,1,1,1,0,9,9], Subs=[(0,2,3),(4,8,5),(10,11,2)], Longest=(4,8,5)
# Example 2: Input=[2,2,0,2,2,2,2,0,0,0,0,0], Expected=[2,2,0,1,1,1,1,0,0,0,0,0], Subs=[(0,1,2),(3,6,4)], Longest=(3,6,4)
# Example 3: Input=[2,2,0,0,0,2,2,2,2,0,2,2], Expected=[2,2,0,0,0,1,1,1,1,0,2,2], Subs=[(0,1,2),(5,8,4),(10,11,2)], Longest=(5,8,4)
# Example 4: Input=[7,7,7,7,0,0,7,7,7,7,7,7], Expected=[7,7,7,7,0,0,1,1,1,1,1,1], Subs=[(0,3,4),(6,11,6)], Longest=(6,11,6)
# Example 5: Input=[8,8,0,8,8,0,8,8,8,8,8,8], Expected=[8,8,0,8,8,0,1,1,1,1,1,1], Subs=[(0,1,2),(3,4,2),(6,11,6)], Longest=(6,11,6)
# Example 6: Input=[5,5,5,0,0,0,5,5,5,5,5,5], Expected=[5,5,5,0,0,0,1,1,1,1,1,1], Subs=[(0,2,3),(6,11,6)], Longest=(6,11,6)
# Example 7: Input=[5,5,5,5,5,0,0,5,5,0,0,0], Expected=[1,1,1,1,1,0,0,5,5,0,0,0], Subs=[(0,4,5),(7,8,2)], Longest=(0,4,5)