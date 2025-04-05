```python
import math
# numpy is not strictly necessary for this task, but can be useful for array operations
# import numpy as np

"""
Transforms an input sequence (list) of integers based on the following rules:
1. Examine the first number in the input sequence.
2. Create a copy of the input sequence.
3. Find the indices of all non-zero numbers.
4. If there are fewer than two non-zero numbers, return the copy (no filling possible between non-zeros).
5. Determine the fill rule:
    - If the first number of the original input sequence is 5, use "Backward Fill".
    - Otherwise, use "Forward Fill".
6. Iterate through consecutive pairs of non-zero indices found in step 3 (let them be idx_left and idx_right).
7. For each pair, fill the elements in the copied sequence *between* these indices (from idx_left + 1 up to idx_right - 1).
    - If using Backward Fill, fill with the value of the element at idx_right in the original sequence.
    - If using Forward Fill, fill with the value of the element at idx_left in the original sequence.
8. Zeros before the first non-zero number and zeros after the last non-zero number remain unchanged by this process.
9. Return the modified sequence.
"""

def find_non_zero_indices(data_list):
  """Helper function: Finds the indices of all non-zero elements in a list."""
  return [i for i, x in enumerate(data_list) if x != 0]

def transform(input_grid):
    """
    Applies the transformation rule to the input list of integers ('input_grid').
    """
    # Handle edge case: empty input
    if not input_grid:
        return []

    # Initialize output_grid as a copy of the input grid to modify
    output_grid = list(input_grid)

    # Find indices of all non-zero elements in the original input
    non_zero_indices = find_non_zero_indices(input_grid)

    # If there are 0 or 1 non-zero numbers, no filling *between* non-zeros can occur.
    # Leading/trailing zeros are already preserved in the copy.
    if len(non_zero_indices) < 2:
        return output_grid # Return the unmodified copy

    # Determine the fill rule based on the value of the first element
    use_backward_fill = (input_grid[0] == 5)

    # Iterate through consecutive pairs of non-zero indices
    # e.g., if indices are [2, 5, 8], pairs will be (2, 5) and (5, 8)
    for i in range(len(non_zero_indices) - 1):
        idx_left = non_zero_indices[i]      # Index of the left non-zero number in the pair
        idx_right = non_zero_indices[i+1]   # Index of the right non-zero number in the pair

        # Check if there is at least one element between the two non-zero numbers
        if idx_right > idx_left + 1:
            # Determine the value to use for filling based on the rule
            if use_backward_fill:
                # Backward Fill: use the value of the right non-zero neighbor
                fill_value = input_grid[idx_right]
            else:
                # Forward Fill: use the value of the left non-zero neighbor
                fill_value = input_grid[idx_left]

            # Fill the elements in the output_grid located between the non-zero neighbors.
            # These elements must originally be zeros, otherwise they would be in non_zero_indices.
            for j in range(idx_left + 1, idx_right):
                output_grid[j] = fill_value

    # Return the modified grid
    return output_grid
```