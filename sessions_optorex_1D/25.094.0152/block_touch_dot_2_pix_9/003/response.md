```python
"""
Transforms a sequence (list) of 12 integers based on the rules derived from examples.

1. Finds the index of the first and last non-zero numbers in the sequence.
2. Identifies and counts the number of zeros located strictly between these first and last non-zero numbers ('intermediate zeros').
3. Based on the count of intermediate zeros:
    - If the count is 0, the sequence remains unchanged.
    - If the count is 1, the single intermediate zero is removed, and one zero is added:
        - to the beginning of the sequence if the first non-zero number was originally at index 0.
        - to the end of the sequence otherwise.
    - If the count is 2 or more, the first two intermediate zeros encountered (based on their original index) are removed, and two zeros are added:
        - to the beginning of the sequence if the first non-zero number was originally at index 3 or greater.
        - to the end of the sequence otherwise (index 0, 1, or 2).
4. Returns the transformed sequence as a list of integers.
"""

# No external libraries are strictly needed for this logic.
# import numpy as np # Not used in this version

def find_first_last_nonzero_indices(seq):
    """
    Finds the index of the first and last non-zero elements in a list.

    Args:
        seq: A list of numbers.

    Returns:
        A tuple (first_nz_idx, last_nz_idx).
        Returns (None, None) if no non-zero elements are found.
        Returns (idx, idx) if only one non-zero element is found at index idx.
    """
    first_nz_idx = None
    last_nz_idx = None
    for i, val in enumerate(seq):
        if val != 0:
            if first_nz_idx is None: # Found the first non-zero
                first_nz_idx = i
            last_nz_idx = i # Keep updating last non-zero index found so far
    return first_nz_idx, last_nz_idx

def transform(input_grid: list) -> list:
    """
    Applies the transformation logic to the input list of integers.
    """
    # Initialize output_grid as a copy of input_grid initially
    output_grid = list(input_grid)

    # Step 1 & 2 (partially): Find the index of the first non-zero element (`first_nz_idx`)
    # and the last non-zero element (`last_nz_idx`).
    first_nz_idx, last_nz_idx = find_first_last_nonzero_indices(input_grid)

    # Handle edge case: no non-zero elements or only one non-zero element (no 'between')
    # In these cases, there are no intermediate zeros, so the sequence is unchanged.
    if first_nz_idx is None or first_nz_idx == last_nz_idx:
        return output_grid # Return the original list copy

    # Step 2 (continued): Identify intermediate zeros and their indices
    # Iterate only between the first and last non-zero elements.
    intermediate_zero_indices = []
    for i in range(first_nz_idx + 1, last_nz_idx):
        if input_grid[i] == 0:
            intermediate_zero_indices.append(i)
            
    intermediate_zero_count = len(intermediate_zero_indices)

    # Step 3: Apply transformation based on the count of intermediate zeros

    # Case 1: intermediate_zero_count == 0
    # (Handled by initialization - no changes needed)
    if intermediate_zero_count == 0:
        pass # output_grid is already a copy of input_grid

    # Case 2: intermediate_zero_count == 1
    elif intermediate_zero_count == 1:
        # Get the index (`k`) of the single intermediate zero.
        zero_idx_to_remove = intermediate_zero_indices[0]
        # Create a temporary sequence by removing the element at index `k`.
        temp_grid = [val for i, val in enumerate(input_grid) if i != zero_idx_to_remove]
        # Determine padding location based on `first_nz_idx`.
        if first_nz_idx == 0:
            # Pad start
            output_grid = [0] + temp_grid
        else:
            # Pad end
            output_grid = temp_grid + [0]

    # Case 3: intermediate_zero_count >= 2
    else: # intermediate_zero_count >= 2
        # Get the indices of the *first two* intermediate zeros to remove.
        zero_idx1_to_remove = intermediate_zero_indices[0]
        zero_idx2_to_remove = intermediate_zero_indices[1]
        # Create a temporary sequence excluding these two specific zeros.
        # Use a set for efficient lookup when building the new list
        indices_to_remove = {zero_idx1_to_remove, zero_idx2_to_remove}
        temp_grid = [val for i, val in enumerate(input_grid) if i not in indices_to_remove]
        
        # Determine padding location based on `first_nz_idx`.
        if first_nz_idx >= 3:
             # Pad start with two zeros
            output_grid = [0, 0] + temp_grid
        else:
            # Pad end with two zeros
            output_grid = temp_grid + [0, 0]

    # Return the final transformed list
    return output_grid
```