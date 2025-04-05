```python
import numpy as np

"""
Transforms a 1D NumPy array of digits by finding the first contiguous block of non-zero digits, 
shifting this block 3 positions to the left (or to the beginning if the shift exceeds the boundary), 
and padding the remaining positions with zeros. The array length remains constant.
"""

def _find_first_non_zero_block(sequence: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end (exclusive) indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise (None, None).
        end_index is the index *after* the last non-zero digit in the block.
    """
    start_index = None
    end_index = None
    non_zero_indices = np.where(sequence != 0)[0]

    # 2. Scan the input list from left to right to find the starting index (`start_in`)
    if len(non_zero_indices) > 0:
        start_index = non_zero_indices[0]

        # 4. If a non-zero digit is found at `start_in`, continue scanning...
        # Find the index of the first zero *after* the start_index
        first_zero_after_start_indices = np.where(sequence[start_index:] == 0)[0]
        if len(first_zero_after_start_indices) > 0:
            # Calculate absolute index
            end_index = start_index + first_zero_after_start_indices[0]
        else:
            # Block runs to the end of the sequence
            end_index = len(sequence)
    
    # 3. If no non-zero digit is found... (handled by returning None, None)
    return start_index, end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the leftward shift transformation to the input sequence.

    Args:
        input_grid: A 1D NumPy array representing the input sequence of digits.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # 1. Input is implicitly parsed into a NumPy array (input_grid)
    n = len(input_grid)

    # 2, 4. Find the first non-zero block indices
    start_in, end_in = _find_first_non_zero_block(input_grid)

    # 3. If no non-zero digit is found, the output is a sequence of n zeros.
    if start_in is None:
        return np.zeros(n, dtype=input_grid.dtype)

    # 5. Extract the non-zero block
    non_zero_block = input_grid[start_in:end_in]
    block_len = len(non_zero_block) # or end_in - start_in

    # 6. Calculate the target starting index (`start_out`)
    start_out = max(0, start_in - 3)

    # 7. Create a new output list (array) of n zeros.
    output_grid = np.zeros(n, dtype=input_grid.dtype)

    # 8. Calculate the target ending index (`end_out`)
    end_out = start_out + block_len

    # 9. Copy the extracted non-zero block into the output list (array)
    # Ensure placement doesn't exceed bounds (numpy slicing handles this safely)
    output_grid[start_out:end_out] = non_zero_block

    # 10, 11. Return the resulting array (formatting to string is handled outside)
    return output_grid
```