import copy

"""
Transforms a single-row input grid by identifying contiguous horizontal blocks of blue pixels (1). 
White pixels (0) remain unchanged. Blue pixels (1) are recolored based on the length of the block they belong to:
- Length 1: become red (2)
- Length 2: become maroon (9)
- Length 3: become gray (5)
Blocks of other lengths (if any) are assumed to remain unchanged based on the examples.
"""

def _find_block_length(row, start_index, color_to_find):
    """
    Finds the length of a contiguous block of a specific color starting at a given index.

    Args:
        row: The list representing the row of pixels.
        start_index: The index where the block potentially starts.
        color_to_find: The color value of the block to measure.

    Returns:
        The length of the contiguous block. Returns 0 if the color at start_index doesn't match.
    """
    length = 0
    n = len(row)
    if row[start_index] != color_to_find:
        return 0
        
    j = start_index
    while j < n and row[j] == color_to_find:
        length += 1
        j += 1
    return length

def transform(input_grid):
    """
    Applies the color transformation rule based on block length to a single-row grid.

    Args:
        input_grid: A list containing a single list of integers (representing a 1xN grid).

    Returns:
        A list containing a single list of integers representing the transformed 1xN grid.
    """
    # Ensure input is a list containing one list (the row)
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle unexpected input format if necessary, though examples suggest single row format.
        # For robustness, could return input or raise error. Sticking to expected format for now.
        print("Warning: Input grid format might be unexpected. Expecting a list containing one list.")
        # Fallback or error handling could go here. Let's assume correct format based on task desc.
        if not input_grid or not isinstance(input_grid, list):
             raise ValueError("Invalid input: input_grid must be a list.")
        if len(input_grid) == 0:
             raise ValueError("Invalid input: input_grid cannot be empty.")
        if not isinstance(input_grid[0], list):
            # Maybe it's a flat list? Try to handle this specific case seen in testing.
            input_row = input_grid 
        else:
            input_row = input_grid[0] # Standard case
    else:
         input_row = input_grid[0]


    # Initialize output_row as a copy of the input row
    output_row = list(input_row) # Use list() for a shallow copy, sufficient for list of ints
    n = len(output_row)
    
    # Define the mapping from block length to output color
    color_map = {
        1: 2,  # Red
        2: 9,  # Maroon
        3: 5   # Gray
    }
    
    i = 0
    # Iterate through the row
    while i < n:
        pixel_color = input_row[i]
        
        # Check if the current pixel is blue (1), indicating a potential block start
        if pixel_color == 1:
            # Find the length of the contiguous block of blue pixels starting at index i
            block_length = _find_block_length(input_row, i, 1)
            
            # Check if this block length has a defined transformation
            if block_length in color_map:
                output_color = color_map[block_length]
                # Apply the transformation to the corresponding pixels in the output row
                for k in range(i, i + block_length):
                    output_row[k] = output_color
            # Else: If block_length is not 1, 2, or 3, the pixels remain 1 (as initially copied).
            
            # Advance the index past the processed block
            i += block_length
        else:
            # If the pixel is not blue (must be white/0 based on examples),
            # it remains unchanged (already copied), so just move to the next pixel.
            i += 1
            
    # Return the transformed row, wrapped in a list to match the required output format
    return [output_row]