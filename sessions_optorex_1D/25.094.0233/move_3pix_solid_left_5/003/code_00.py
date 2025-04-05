"""
Identify the contiguous block of identical non-zero digits in the input NumPy array.
Shift this block 3 positions to the left to create the output array. 
If shifting left would result in a start index less than 0, the block starts at index 0. 
The length and data type of the array, as well as the composition (non-zero digit value, 
block length, number of zeros) are preserved.
"""

import numpy as np

def find_non_zero_block_np(data):
    """
    Finds the first contiguous block of identical non-zero digits in a 1D NumPy array.

    Args:
        data: A 1D NumPy array of integers.

    Returns:
        A tuple containing:
        - The non-zero digit value (int).
        - The length of the block (int).
        - The starting index of the block (int).
        Returns (None, 0, -1) if no non-zero block is found or the array is empty/None.
    """
    # Handle empty, None, or all-zero arrays
    if data is None or len(data) == 0 or np.all(data == 0):
        return None, 0, -1

    start_index = -1
    block_value = None
    length = 0
    
    # Find changes in the array to identify potential block boundaries
    # Pad with 0 at start/end to catch blocks at edges
    padded_data = np.concatenate(([0], data, [0])) 
    diff = np.diff(padded_data)
    starts = np.where(diff > 0)[0] # Indices in original data where a block might start
    ends = np.where(diff < 0)[0]   # Indices in original data where a block might end

    # Iterate through potential blocks to find the first non-zero one
    for s, e in zip(starts, ends):
        if data[s] != 0: # Found the first non-zero block
            block_value = data[s]
            length = e - s
            start_index = s
            break # Assume only one block per sequence based on examples
            
    # Check if a block was actually found (safeguard)
    if block_value is None: 
         return None, 0, -1
         
    return block_value, int(length), int(start_index) # Return standard int types

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D NumPy array by shifting the non-zero block left by 3 positions.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the transformed sequence.
    """
    # Get the size and data type of the input array
    n = len(input_grid)
    dtype = input_grid.dtype 

    # Find the non-zero block in the input
    block_value, block_length, start_index_input = find_non_zero_block_np(input_grid)

    # Initialize output_grid with zeros, matching input size and type
    output_grid = np.zeros(n, dtype=dtype)

    # If a non-zero block was found, place it in the output grid
    if block_value is not None:
        # Calculate the target starting index, ensuring it's not negative
        start_index_output = max(0, start_index_input - 3)
        
        # Calculate the end index for slicing, ensuring it doesn't exceed array bounds
        end_index_output = min(n, start_index_output + block_length)
        
        # Place the block into the output grid
        output_grid[start_index_output:end_index_output] = block_value

    # Return the transformed grid
    return output_grid