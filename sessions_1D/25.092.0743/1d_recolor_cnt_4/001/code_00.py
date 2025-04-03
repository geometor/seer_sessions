import numpy as np
from typing import List

"""
Processes a 1xN grid (represented as a list containing a single list).
Identifies contiguous horizontal segments (blocks) of gray (5) pixels in the single row.
Replaces the gray pixels in each block with a new color based on the block's length:
- Length 1: Replace with yellow (4)
- Length 2: Replace with blue (1)
- Length 3: Replace with green (3)
White (0) pixels remain unchanged. If a gray block has a length other than 1, 2, or 3, 
it remains gray (5).
"""

def transform(input_grid_nested: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the length of contiguous gray blocks.

    Args:
        input_grid_nested: A list containing one list (the row) representing the 1xN input grid. 
                           Example: [[0, 5, 0, 5, 5, 5, 0]]

    Returns:
        A list containing one list representing the 1xN output grid.
    """
    # Ensure input is not empty and has the expected structure
    if not input_grid_nested or not isinstance(input_grid_nested, list) or not input_grid_nested[0] or not isinstance(input_grid_nested[0], list):
        # Return empty or handle error appropriately based on requirements
        return [[]] 
        
    # Extract the single row from the nested list structure
    input_row = input_grid_nested[0]
    
    # Convert the row to a NumPy array for efficient processing
    input_array = np.array(input_row, dtype=int)
    
    # Create a copy of the input array to modify, preserving original structure and non-target pixels
    output_array = np.copy(input_array)
    
    # Get the width (number of columns) of the grid
    width = len(input_array)
    
    # Initialize index for iterating through the grid row
    i = 0
    # Iterate through the grid row pixel by pixel
    while i < width:
        # Check if the current pixel is gray (color code 5)
        if input_array[i] == 5:
            # Start of a potential gray block found
            start_index = i
            block_length = 0
            
            # Measure the length of the contiguous gray block
            j = i
            while j < width and input_array[j] == 5:
                block_length += 1
                j += 1
            
            # Determine the replacement color based on the measured block length
            # Default to the original color (gray 5) if length doesn't match rules
            replacement_color = 5 
            if block_length == 1:
                replacement_color = 4 # Yellow for length 1
            elif block_length == 2:
                replacement_color = 1 # Blue for length 2
            elif block_length == 3:
                replacement_color = 3 # Green for length 3
            
            # Fill the corresponding section in the output array with the determined replacement color
            # This loop runs from the start index for the duration of the block length
            for k in range(start_index, start_index + block_length):
                output_array[k] = replacement_color
            
            # Advance the main loop index to the position immediately after the processed block
            # This avoids reprocessing pixels within the same block
            i = start_index + block_length 
        else:
            # If the current pixel is not gray (must be white, 0, based on examples),
            # simply move to the next pixel. The white pixel is already correct in the output_array copy.
            i += 1
            
    # Convert the modified NumPy array back to a standard Python list
    output_row = output_array.tolist()
    
    # Wrap the resulting row list in another list to match the expected ARC output format [[...]]
    return [output_row]
