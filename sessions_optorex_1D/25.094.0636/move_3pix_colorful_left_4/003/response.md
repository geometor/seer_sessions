```python
import numpy as np

"""
Transforms a 1D NumPy array of digits by finding the first contiguous block of non-zero digits, 
shifting this block 3 positions to the left (or to the beginning if the shift exceeds the boundary), 
and padding the remaining positions with zeros. The array length remains constant.
"""

def _find_first_non_zero_block(sequence):
    """
    Finds the start and end indices (exclusive) of the first contiguous block of non-zero numbers.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise (None, None).
        end_index is the index *after* the last non-zero digit in the block.
    """
    start_index = -1
    # Find the start of the block
    non_zero_indices = np.where(sequence != 0)[0] # Get indices of all non-zero elements
    if len(non_zero_indices) == 0:
        return None, None # No non-zero elements found

    start_index = non_zero_indices[0] # First non-zero index is the start

    # Find the end of the block (the first zero *after* the start, or end of list)
    end_index = len(sequence) # Default to end of list if no zero follows
    # Search for the first zero starting from the position after the block begins
    zero_indices_after_start = np.where(sequence[start_index + 1:] == 0)[0]
    if len(zero_indices_after_start) > 0:
        # The index found is relative to the slice start (start_index + 1)
        # Add back the offset to get the absolute index in the original sequence
        end_index = start_index + 1 + zero_indices_after_start[0]

    return start_index, end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array sequence of digits.

    Args:
        input_grid: A 1D NumPy array of digits.

    Returns:
        A 1D NumPy array of digits representing the transformed sequence.
    """
    # 1. Receive the input NumPy array of digits.
    # input_grid is the input

    # 2. Determine the length (`n`) of the input array.
    n = len(input_grid)

    # 3. Scan the input array to find the start and end indices of the first non-zero block.
    start_index, end_index = _find_first_non_zero_block(input_grid)

    # 4. If no non-zero digit is found, return an array containing all zeros.
    if start_index is None:
        return np.zeros(n, dtype=input_grid.dtype) # Match input dtype

    # 5. Extract the contiguous block of non-zero digits.
    # Note: end_index from _find_first_non_zero_block is exclusive.
    non_zero_block = input_grid[start_index:end_index]

    # 6. Calculate the target starting index (`target_start_index`) for this block.
    # Shift left by 3, but not before index 0.
    target_start_index = max(0, start_index - 3)

    # 7. Create a new NumPy array (`output_grid`) initialized with zeros.
    output_grid = np.zeros(n, dtype=input_grid.dtype) # Match input dtype

    # 8. Calculate the target ending index and place the block.
    block_len = len(non_zero_block)
    # Ensure the block fits within the array bounds when placed.
    target_end_index = target_start_index + block_len
    # This check is slightly redundant given fixed length and how slicing works, but safe.
    # If target_end_index > n, slicing output_grid[target_start_index:target_end_index]
    # would take up to n, and non_zero_block might be truncated if it didn't fit.
    # However, the problem implies the length is fixed and the block always fits after shift.
    output_grid[target_start_index:target_end_index] = non_zero_block

    # 9. Return the output_grid.
    return output_grid
```