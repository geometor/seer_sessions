import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Identify the single contiguous block of non-white (non-zero) pixels in the input row.
2. Determine the start and end indices of this block.
3. Check if the block starts at index 0 (no preceding white pixel) or if there is no space 
   to shift right (block ends at the last index). If either is true, return the input unchanged.
4. Otherwise, create the output row by:
    a. Shifting the entire block one position to the right.
    b. Moving the white pixel (value 0) that was immediately preceding the block 
       (at start_index - 1 in the input) into the original starting position of the block 
       (at start_index in the output).
"""

def find_non_white_block(row: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end index of the first contiguous block of non-white pixels.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                # Mark the start of a potential block
                start_index = i
            # Update the end index as long as we see non-white pixels
            end_index = i 
        elif start_index != -1:
            # We found a white pixel after a block started, so the block ended at i-1
            return start_index, end_index
            
    # If a block started and went to the end of the row
    if start_index != -1:
        return start_index, end_index
        
    # No non-white block found
    return None

def transform(input_grid) -> List[List[int]]:
    """
    Shifts a contiguous block of non-white pixels in a single-row grid one step 
    to the right, moving the preceding white pixel into the block's original start position.

    Args:
        input_grid: A potentially nested list or numpy array representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    
    # --- Input Validation and Initialization ---
    try:
        # Convert to numpy array for robust shape checking
        input_array = np.array(input_grid, dtype=int)
        # Ensure it's a 2D array with exactly one row
        if input_array.ndim != 2 or input_array.shape[0] != 1:
            # Return original input if shape is not 1xN
            return input_grid.tolist() if isinstance(input_grid, np.ndarray) else input_grid
        
        # Get the row as a standard Python list for easier manipulation
        input_row = input_array[0].tolist()
        n = len(input_row)
        # Initialize output_row as a copy of the input row
        output_row = list(input_row) 

    except Exception:
         # Handle potential errors during conversion (e.g., ragged lists)
         # Return the input as is if it's not a valid grid representation.
         # Convert back to list if it was a numpy array initially.
        return input_grid.tolist() if isinstance(input_grid, np.ndarray) else input_grid

    # --- Find the Non-White Block ---
    block_indices = find_non_white_block(input_row)

    # --- Apply Transformation if Valid ---
    if block_indices:
        start_index, end_index = block_indices
        
        # Check conditions for transformation:
        # 1. Block must not start at the very beginning (needs preceding white pixel)
        # 2. Block must not end at the very end (needs space to shift right)
        if start_index > 0 and end_index + 1 < n:
            
            # Perform the shift
            # Iterate from the end of the block backwards to avoid overwriting
            for i in range(end_index, start_index - 1, -1):
                output_row[i + 1] = input_row[i]
                
            # Place the preceding white pixel (which is always 0) 
            # at the original start position of the block
            output_row[start_index] = 0 
            # Note: The pixel originally at start_index-1 (which was 0) is effectively
            # overwritten by the start of the shifted block at output_row[start_index+1],
            # and the pixel originally at start_index is moved to start_index+1.
            # The pixel at end_index+1 (which was 0) is overwritten by the end of the block.
            # The original start_index position gets the 0. This matches the examples.

    # --- Format and Return Output ---
    # Wrap the output row back into the grid format (list of lists)
    output_grid = [output_row]
    return output_grid