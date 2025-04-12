import numpy as np

# Reusing the _find_best_pattern from the previous attempt (code_00.py)
# Note: numpy is not actually used in this specific helper function
def _find_best_pattern_unlimited(segment: list[int]) -> list[int] | None:
    n = len(segment)
    if n == 0:
        return None
    best_pattern = None
    max_score = -1
    min_len_for_max_score = float('inf')
    # NO MAX LENGTH LIMIT HERE
    for length in range(1, n + 1): # <= Search up to full length
        for i in range(n - length + 1):
            candidate_pattern = segment[i : i + length]
            current_score = 0
            for j in range(n):
                if segment[j] == candidate_pattern[j % length]:
                    current_score += 1
            if current_score > max_score:
                max_score = current_score
                best_pattern = candidate_pattern
                min_len_for_max_score = length
            elif current_score == max_score:
                if length < min_len_for_max_score:
                    best_pattern = candidate_pattern
                    min_len_for_max_score = length
    return best_pattern

# Now define the _find_best_pattern with the proposed fix (max length limit)
def _find_best_pattern_limited(segment: list[int]) -> list[int] | None:
    n = len(segment)
    if n == 0:
        return None
    best_pattern = None
    max_score = -1
    min_len_for_max_score = float('inf')
    # APPLY MAX LENGTH LIMIT HERE
    max_pattern_len = min(n, 8) # Limit search to length 8
    for length in range(1, max_pattern_len + 1): # <= Limit applied
        for i in range(n - length + 1):
            candidate_pattern = segment[i : i + length]
            current_score = 0
            for j in range(n):
                if segment[j] == candidate_pattern[j % length]:
                    current_score += 1
            if current_score > max_score:
                max_score = current_score
                best_pattern = candidate_pattern
                min_len_for_max_score = length
            elif current_score == max_score:
                if length < min_len_for_max_score:
                    best_pattern = candidate_pattern
                    min_len_for_max_score = length
    return best_pattern

# Example 1, Row 2 Segment
segment_ex1_r2 = [1, 3, 1, 3, 1, 3, 3, 3, 1]

# Example 2, Row 12 Segment
segment_ex2_r12 = [8, 4, 4, 8, 8, 4, 8, 8, 8, 4, 8, 8, 8, 4, 8, 8, 8, 4]

# Example 2, Row 13 Segment
segment_ex2_r13 = [8, 8, 4, 4, 8, 8, 8, 4, 8, 8, 8, 4, 8, 8, 8, 4, 8, 8]

# Test Example 1
pattern_unlimited_ex1 = _find_best_pattern_unlimited(segment_ex1_r2)
pattern_limited_ex1 = _find_best_pattern_limited(segment_ex1_r2)
expected_pattern_ex1 = [1, 3]
print(f"Example 1, Row 2:")
print(f"  Segment: {segment_ex1_r2}")
print(f"  Pattern (Unlimited): {pattern_unlimited_ex1}")
print(f"  Pattern (Limited 8): {pattern_limited_ex1}")
print(f"  Expected Pattern:    {expected_pattern_ex1}")
print(f"  Unlimited match expected? {pattern_unlimited_ex1 == expected_pattern_ex1}")
print(f"  Limited match expected?   {pattern_limited_ex1 == expected_pattern_ex1}")

# Test Example 2, Row 12
pattern_unlimited_ex2_r12 = _find_best_pattern_unlimited(segment_ex2_r12)
pattern_limited_ex2_r12 = _find_best_pattern_limited(segment_ex2_r12)
expected_pattern_ex2_r12 = [8, 4, 8, 8] # As determined previously
print(f"\nExample 2, Row 12:")
print(f"  Segment: {segment_ex2_r12}")
print(f"  Pattern (Unlimited): {pattern_unlimited_ex2_r12}")
print(f"  Pattern (Limited 8): {pattern_limited_ex2_r12}")
print(f"  Expected Pattern:    {expected_pattern_ex2_r12}")
print(f"  Unlimited match expected? {pattern_unlimited_ex2_r12 == expected_pattern_ex2_r12}")
print(f"  Limited match expected?   {pattern_limited_ex2_r12 == expected_pattern_ex2_r12}")

# Test Example 2, Row 13
pattern_unlimited_ex2_r13 = _find_best_pattern_unlimited(segment_ex2_r13)
pattern_limited_ex2_r13 = _find_best_pattern_limited(segment_ex2_r13)
expected_pattern_ex2_r13 = [8, 8, 8, 4] # As determined previously
print(f"\nExample 2, Row 13:")
print(f"  Segment: {segment_ex2_r13}")
print(f"  Pattern (Unlimited): {pattern_unlimited_ex2_r13}")
print(f"  Pattern (Limited 8): {pattern_limited_ex2_r13}")
print(f"  Expected Pattern:    {expected_pattern_ex2_r13}")
print(f"  Unlimited match expected? {pattern_unlimited_ex2_r13 == expected_pattern_ex2_r13}")
print(f"  Limited match expected?   {pattern_limited_ex2_r13 == expected_pattern_ex2_r13}")
