```python
import numpy as np

"""
Transforms a 1D NumPy integer array by identifying the first contiguous block of 
non-zero numbers and shifting this block exactly 3 positions to the right within 
an array of the same fixed length (12), padding the remaining positions with zeros.
If no non-zero block is found, an all-zero array is returned.
"""

def find_first_non_zero_block(grid):
    """
    Finds the start and end indices (exclusive) of the first contiguous block of non-zero numbers.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise (None, None).
    """
    start_index = None
    end_index = None
    n = len(grid)

    for i, val in enumerate(grid):
        if val != 0:
            # Found a non-zero value
            if start_index is None:
                # Mark the start of the first block found
                start_index = i
            # Continue checking or update end index if block extends
        elif start_index is not None:
            # Found a zero *after* the block started, so the block ends at index i
            end_index = i
            break # Stop searching once the first block is fully identified

    # Handle case where the block extends to the very end of the grid
    if start_index is not None and end_index is None:
        end_index = n

    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 1D NumPy array of integers (assumed length 12 based on examples).

    Returns:
        A new 1D NumPy array representing the transformed grid.
    """
    # Define sequence length and shift amount
    sequence_length = len(input_grid)
    shift_amount = 3

    # Initialize the output grid with zeros, matching input shape and type
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block of non-zero numbers in the input
    start_index, end_index = find_first_non_zero_block(input_grid)

    # If a non-zero block was found (start_index is not None)
    if start_index is not None:
        # Extract the non-zero block
        non_zero_block = input_grid[start_index:end_index]
        
        # Calculate the new starting position for the block
        new_start_index = start_index + shift_amount
        
        # Calculate the length of the block
        block_len = len(non_zero_block)

        # Calculate the theoretical new ending position (exclusive)
        new_end_index = new_start_index + block_len
        
        # --- Place the non_zero_block into the output grid at the new position ---
        
        # Check if the block starts within the grid bounds
        if new_start_index < sequence_length:
            # Determine the actual end index, ensuring it doesn't exceed grid length
            actual_new_end = min(new_end_index, sequence_length)
            
            # Determine the length of the block segment that actually fits
            effective_block_length = actual_new_end - new_start_index
            
            # Copy the fitting part of the block to the output grid
            output_grid[new_start_index : actual_new_end] = non_zero_block[:effective_block_length]
            
    # If no non-zero block was found, the output grid remains all zeros, which is the correct default state.
    
    return output_grid
```