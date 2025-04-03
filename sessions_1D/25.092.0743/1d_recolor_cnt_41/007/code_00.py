import copy

"""
Replace contiguous horizontal blocks of yellow (4) pixels within a single-row list (representing a 1xN grid) with a new color determined by the block's length. 
Blocks of length 1 become maroon (9), length 2 become magenta (6), and length 3 become green (3). 
White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input list (representing a 1xN grid) by replacing yellow blocks based on length.

    Args:
        input_grid (list[int]): A 1D list of integers representing the input grid row.

    Returns:
        list[int]: A 1D list representing the transformed output grid row.
    """
    # Ensure input is a list, handle potential errors if needed, though ARC expects valid input.
    if not isinstance(input_grid, list):
        # Handle error or return input unchanged
        return copy.deepcopy(input_grid) 

    # Initialize output_grid as a copy of the input list
    output_grid = list(input_grid) 
    width = len(input_grid)
    col = 0

    # Iterate through the list to find and replace yellow blocks
    while col < width:
        # Check if the current pixel is yellow (4)
        if input_grid[col] == 4:
            # Found the start of a potential yellow block
            start_col = col
            block_length = 0
            
            # Scan ahead to count consecutive yellow pixels starting from start_col
            scan_col = start_col
            while scan_col < width and input_grid[scan_col] == 4:
                block_length += 1
                scan_col += 1 # Advance scan pointer

            # Determine the replacement color based on block length
            replacement_color = -1 # Sentinel value indicating no replacement rule matched
            if block_length == 1:
                replacement_color = 9 # Maroon
            elif block_length == 2:
                replacement_color = 6 # Magenta
            elif block_length == 3:
                replacement_color = 3 # Green
            
            # Apply the replacement color to the output_grid for the identified block range
            # This modification happens only if a replacement rule was found (length 1, 2, or 3)
            if replacement_color != -1:
                # Modify the output_grid in the range [start_col, start_col + block_length)
                for i in range(start_col, start_col + block_length):
                    # Ensure we don't write past the end of the list (though logic should prevent this)
                    if i < width: 
                        output_grid[i] = replacement_color
            
            # Advance the main loop counter 'col' past the block we just processed
            # scan_col is already pointing to the first element *after* the block
            col = scan_col 
            
            # Continue to the next iteration without the default increment at the end
            continue 

        # If the current pixel is not yellow (it must be white (0) based on input colors), 
        # simply move to the next column
        col += 1
        
    # Return the modified list
    return output_grid