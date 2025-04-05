import numpy as np
import math

"""
The transformation rule takes a 1D NumPy array of integers, identifies a 
contiguous block of a single non-zero digit, and shifts this entire block two 
positions to the right within the array. The original positions of the block 
are replaced with zeros, and the array length remains constant.
"""

def _find_non_zero_block_indices(arr: np.ndarray) -> tuple[int | None, int, int]:
    """
    Finds the non-zero value and the start/end indices of its contiguous block.
    
    Args:
        arr: The input 1D NumPy array.
        
    Returns:
        A tuple containing:
        - The non-zero value (or None if all zeros).
        - The starting index of the block (or -1 if not found).
        - The ending index of the block (or -1 if not found).
    """
    # Find indices of non-zero elements
    non_zero_indices = np.where(arr != 0)[0]

    # Handle case where the array is all zeros
    if len(non_zero_indices) == 0:
        return None, -1, -1

    # Get the non-zero value (assuming only one unique non-zero value exists per block)
    non_zero_value = int(arr[non_zero_indices[0]]) 
    
    # Find the start and end index of the contiguous block
    start_index = np.min(non_zero_indices)
    end_index = np.max(non_zero_indices)
    
    # Verify contiguity (optional but good practice for complex cases)
    # expected_length = end_index - start_index + 1
    # if len(non_zero_indices) != expected_length:
    #     # This would indicate multiple blocks or gaps, which isn't expected 
    #     # based on the examples, but could be handled if needed.
    #     print("Warning: Non-contiguous block or multiple non-zero values detected.")
        
    return non_zero_value, int(start_index), int(end_index)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: shifts the non-zero block two steps right.

    Args:
        input_grid: The input 1D NumPy array.

    Returns:
        The transformed 1D NumPy array.
    """
    # Get the shape (length) of the input array
    n = input_grid.shape[0]
    
    # Initialize the output grid with zeros, matching input size and type
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero block details
    non_zero_value, start_index, end_index = _find_non_zero_block_indices(input_grid)

    # If a non-zero block was found, perform the shift
    if non_zero_value is not None:
        # Define the shift amount
        shift = 2
        
        # Calculate the new start and end indices
        new_start_index = start_index + shift
        new_end_index = end_index + shift

        # Populate the output grid with the shifted block
        # Iterate through the indices that *should* be filled in the output
        for i in range(new_start_index, new_end_index + 1):
             # Check bounds: only write if the index is valid for the output grid
             if 0 <= i < n:
                 output_grid[i] = non_zero_value

    return output_grid