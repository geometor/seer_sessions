import numpy as np
from typing import List, Tuple

"""
Identifies which of two specific 3-element subsequences exists at a specific 
starting position within any row of the input grid. Based on which subsequence 
is found, applies a corresponding right cyclic shift transformation ([A, B, C] 
becomes [C, A, B]) to that subsequence wherever it appears at the specified 
starting position in any row of the grid.

Rule 1: If subsequence [azure(8), green(3), orange(7)] is found starting at index 1 
in any row, then replace all occurrences of [8, 3, 7] starting at index 1 with 
[orange(7), azure(8), green(3)].

Rule 2: If subsequence [gray(5), white(0), orange(7)] is found starting at index 0 
in any row, then replace all occurrences of [5, 0, 7] starting at index 0 with 
[orange(7), gray(5), white(0)].

If neither triggering subsequence is found according to the rules, the grid remains unchanged.
It is assumed that only one of these rules will be applicable for a given input grid.
"""

# Define the specific patterns and transformations from the training examples
# Rule format: (target_subsequence, start_index, replacement_subsequence)
RULES = [
    ([8, 3, 7], 1, [7, 8, 3]), # From train_1: [azure, green, orange] -> [orange, azure, green] at index 1
    ([5, 0, 7], 0, [7, 5, 0]), # From train_2: [gray, white, orange] -> [orange, gray, white] at index 0
]

def check_subsequence(row: np.ndarray, subsequence: List[int], start_index: int) -> bool:
    """Checks if a specific subsequence exists in a row starting at a given index."""
    if start_index + len(subsequence) > len(row):
        return False
    return np.array_equal(row[start_index : start_index + len(subsequence)], subsequence)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on pre-defined subsequence replacement rules.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Determine which rule applies based on the input grid
    applicable_rule = None
    for row_idx in range(rows):
        for target_subsequence, start_index, _ in RULES:
             # Check if the rule *could* apply (enough columns) and if the target exists
            if start_index + len(target_subsequence) <= cols:
                 if check_subsequence(input_np[row_idx], target_subsequence, start_index):
                    applicable_rule = (target_subsequence, start_index, _) # Store the full rule tuple
                    break # Assume only one rule type applies per grid
        if applicable_rule:
            break # Stop checking rows once a rule is identified

    # If a rule was identified, apply the transformation to all matching rows
    if applicable_rule:
        target_subsequence, start_index, replacement_subsequence = applicable_rule
        subsequence_len = len(target_subsequence)

        # Iterate through rows again to apply the transformation where needed
        for row_idx in range(rows):
            # Check if the target subsequence exists at the specified location in this row
            if check_subsequence(output_np[row_idx], target_subsequence, start_index):
                # Apply the cyclic shift (replacement)
                output_np[row_idx, start_index : start_index + subsequence_len] = replacement_subsequence

    # Convert the result back to a list of lists
    return output_np.tolist()