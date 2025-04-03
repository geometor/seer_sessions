"""
Transforms a 1D grid (represented as a 1xN list of lists) by replacing contiguous 
horizontal blocks of magenta (6) pixels with a new color based on the block's length:
- Blocks of length 1 become red (2).
- Blocks of length 2 become gray (5).
- Blocks of length 3 become azure (8).
White (0) pixels remain unchanged in their original positions. Assumes input contains
only white (0) and magenta (6).
"""

import copy # Used for deep copying the input grid if needed, though list slicing works for 1D copy

def transform(input_grid):
    # Input Validation: Check for empty or improperly formatted grid
    if not isinstance(input_grid, list) or len(input_grid) == 0 or \
       not isinstance(input_grid[0], list):
        # Return invalid input as is or an empty representation
        return input_grid if input_grid != [[]] else [[]] 
        
    # Handle empty row case
    if len(input_grid[0]) == 0:
        return [[]]

    # Extract the single row from the input grid representation
    input_row = input_grid[0]
    
    # Initialize the output row as a copy of the input row.
    # White pixels (0) are already correctly placed by this copy.
    output_row = list(input_row) # Create a shallow copy, sufficient for a list of ints
    
    width = len(input_row)
    i = 0 # Initialize index for iterating through the row

    # Iterate through the row to find and replace magenta blocks
    while i < width:
        # Check if the current pixel is magenta (6)
        if output_row[i] == 6:
            # Found the start of a potential magenta block
            block_start = i
            block_length = 0
            
            # Scan forward to find the end of the contiguous magenta block
            # Use 'j' for scanning to not interfere with the main loop index 'i' yet
            j = i
            while j < width and output_row[j] == 6:
                block_length += 1
                j += 1
                
            # Determine the replacement color based on the measured block length
            replacement_color = -1 # Default value indicates no replacement needed
            if block_length == 1:
                replacement_color = 2 # Red
            elif block_length == 2:
                replacement_color = 5 # Gray
            elif block_length == 3:
                replacement_color = 8 # Azure
            # Note: If blocks of other lengths were found, they would remain magenta (6) 
            # as replacement_color would stay -1. This matches the examples.

            # If a valid replacement color was determined (length was 1, 2, or 3),
            # update the corresponding segment in the output row.
            if replacement_color != -1:
                for k in range(block_start, block_start + block_length):
                    output_row[k] = replacement_color
                    
            # Advance the main loop index 'i' past the processed block
            i = block_start + block_length
            
        else:
            # If the current pixel is not magenta (it's white 0), 
            # simply move to the next pixel.
            i += 1
            
    # Format the final modified row back into the required list-of-lists structure
    output_grid = [output_row]
    
    # Return the transformed grid
    return output_grid