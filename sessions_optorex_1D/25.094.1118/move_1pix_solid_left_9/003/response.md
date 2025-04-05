```python
import numpy as np

"""
Transforms a 1D NumPy array containing a single contiguous block of identical 
non-zero digits, padded with zeros. The transformation shifts the non-zero block 
one position to the left. It assumes the block does not start at index 0 in the input.
The length of the array remains constant, with zeros filling the remaining positions.
"""

def find_non_zero_block_indices(arr):
    """
    Finds the start index, end index (exclusive), and value of the 
    first contiguous block of identical non-zero digits in a NumPy array.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise returns (None, None, None). Returns None if multiple blocks
        or non-contiguous non-zero elements are found.
    """
    # Find all indices where the element is not zero
    non_zero_indices = np.where(arr != 0)[0]

    # If no non-zero elements are found, return None
    if len(non_zero_indices) == 0:
        return None, None, None

    # Determine the start index and the value of the potential block
    start_index = non_zero_indices[0]
    value = arr[start_index]
    
    # Check if the non-zero elements form a single contiguous block
    # and all have the same value
    is_single_contiguous_block = True
    for i in range(len(non_zero_indices)):
        # Check contiguity: current index should be start_index + i
        # Check value: current element should match the first non-zero value
        if non_zero_indices[i] != start_index + i or arr[non_zero_indices[i]] != value:
            is_single_contiguous_block = False
            break
            
    # If it's a valid block, calculate the end index (exclusive)
    if is_single_contiguous_block:
        end_index = start_index + len(non_zero_indices)
        return start_index, end_index, value
    else:
        # If not a single contiguous block of the same value, return None
        return None, None, None


def transform(input_grid):
    """
    Applies the left-shift transformation to the non-zero block.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the size of the input grid
    n = len(input_grid)
    
    # Initialize output_grid with zeros, same shape as input
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block of non-zero digits in the input grid
    start_index, end_index, block_value = find_non_zero_block_indices(input_grid)

    # Check if a valid block was found and if it can be shifted left (start > 0)
    if start_index is not None and start_index > 0:
        # Calculate the new start index (shifted one position left)
        new_start_index = start_index - 1
        # Calculate the new end index (shifted one position left)
        new_end_index = end_index - 1 

        # Fill the corresponding segment in the output grid with the block's value
        # Use slicing for efficient assignment
        output_grid[new_start_index:new_end_index] = block_value
        
    # If no block is found, or if the block starts at index 0 (cannot shift left),
    # the output_grid remains all zeros (as initialized), which matches the 
    # expected behavior based on problem constraints (block always exists and isn't at index 0).
    # If input is all zeros, find_non_zero_block_indices returns None, and output is all zeros.

    return output_grid
```