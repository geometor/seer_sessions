import numpy as np
from typing import List, Tuple

"""
Transforms the input grid by identifying the single contiguous block of 
non-white pixels (color != 0) in the single row and shifting it 2 positions 
to the right. The output grid maintains the original dimensions. If the shifted 
block extends beyond the right boundary, it is clipped. The background is 
white (0). If no block is found, or the input is invalid, a background-filled 
grid of the same dimensions is returned.
"""

def find_colored_block_1d(grid_1d: np.ndarray) -> Tuple[int, int, int]:
    """
    Helper function to find the first contiguous block of non-background color (0) in a 1D grid.

    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A tuple containing:
        - color (int): The color of the block.
        - start_index (int): The starting index of the block.
        - length (int): The length of the block.
        Returns (0, -1, 0) if no non-background block is found.
    """
    start_index = -1
    color = 0
    length = 0
    
    # Iterate through the grid to find the first non-zero pixel sequence
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:  # Found a non-background pixel
            if start_index == -1:  # Start of the first block found
                start_index = i
                color = pixel
                length = 1
            elif pixel == color: # Continuation of the current block
                length += 1
            else: 
                 # If a different non-zero color is found, stop (task assumes one block)
                 break 
        elif start_index != -1:  # Found background (0) after a block had started
            # This signifies the end of the first block
            break  

    # If no block was ever started (start_index remains -1), return indicator values
    if start_index == -1: 
        return 0, -1, 0 # Using color 0, index -1, length 0 to indicate no block

    return color, start_index, length

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list containing a single list of integers representing the 1xN input grid.

    Returns:
        A list containing a single list of integers representing the transformed 1xN grid.
    """
    # --- Input Validation and Preparation ---
    # Ensure input is a list containing exactly one inner list
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
         # Return an empty grid if format is incorrect, matching prior observed failure mode.
         # Consider if returning the original input or raising an error would be better.
         # If the goal is to match dimensions, returning an empty list of list might be wrong.
         # Let's try returning an empty list structure for now, but this is a weak point.
         # A better approach might be to determine expected dimensions if possible, 
         # or signal failure more explicitly if the environment allows.
         # Returning input_grid might be safer if the transformation should do nothing on bad input.
         # Given the test failure producing `[[]]`, let's mimic that for now.
         # If input_grid is like [[1,2,3], [4,5,6]], we also fail here.
         # If input_grid is [], we fail here.
         return [[]] 
         
    # Handle the case where the inner list exists but is empty
    if not input_grid[0]:
        return [[]] # Return empty list of list for an empty inner list
        
    # Convert the inner list (the actual grid row) to a numpy array for efficient manipulation
    try:
        input_row = np.array(input_grid[0], dtype=int)
    except ValueError: # Handle potential errors if inner list contains non-integers
        return [[]] # Return empty on conversion error

    width = len(input_row)

    # --- Core Transformation Logic ---
    # 1. Identify the single contiguous block of non-white pixels using the helper function
    color, start_index, length = find_colored_block_1d(input_row)

    # 2. Create a new output grid (as a numpy array) of the same size, 
    #    initialized with the background color (0)
    output_row = np.zeros_like(input_row) 

    # 3. Check if a block was actually found (start_index != -1)
    if start_index != -1: 
        # Calculate the target starting index for the block by shifting right by 2
        new_start_index = start_index + 2

        # Determine the actual range of indices to write to in the output grid,
        # applying clipping to handle boundary conditions (stay within 0 to width-1).
        # write_start cannot be less than 0
        write_start = max(0, new_start_index) 
        # write_end cannot be greater than the grid width
        write_end = min(width, new_start_index + length) 

        # Place the block (with its original color) into the calculated slice 
        # of the output grid, but only if the calculated range is valid 
        # (i.e., write_start is less than write_end). This prevents errors if the block
        # is shifted completely off the grid to the right.
        if write_start < write_end: 
            output_row[write_start:write_end] = color
    # If no block was found (start_index == -1), the output_row remains all zeros,
    # which is the correct behavior (return a background-filled grid).

    # --- Output Formatting ---
    # Convert the resulting numpy array back into a list of integers
    output_row_list = output_row.tolist()
    
    # Wrap the list in another list to match the required List[List[int]] format.
    output_grid = [output_row_list]

    return output_grid