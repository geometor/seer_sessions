import numpy as np # Although not strictly necessary for list manipulation, it's common in ARC tasks

"""
Transforms a 1xN input grid based on sequences of colored pixels.

The transformation operates on a single-row grid. It iterates through the input row:
1. If a pixel is background (0), it's copied directly to the output.
2. If a non-background pixel (color C) is encountered:
   a. It checks if this pixel is the start of a 3-pixel block of the same color (C, C, C) within the input grid bounds.
   b. If it is an existing 3-pixel block, all three pixels (C, C, C) are copied to the output, and the input index advances by 3.
   c. If it is *not* an existing 3-pixel block (either because the sequence is shorter, the colors differ, or it's near the end of the row), it is treated as a single pixel to be expanded. Three pixels of its color (C, C, C) are appended to the output, and the input index advances by only 1.
The process continues until the entire input row is processed. The output row is then wrapped in a list to maintain the grid format.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list of integers.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Ensure input is a list of lists and extract the single row
    # Handle potential issues like numpy arrays or empty inputs
    if isinstance(input_grid, np.ndarray):
        input_row = input_grid.tolist()[0]
    elif isinstance(input_grid, list) and input_grid:
        input_row = input_grid[0]
    else:
        # Return empty grid for invalid input
        return [[]] 

    width = len(input_row)
    if width == 0:
        return [[]] # Handle empty row case

    # Initialize output row list
    output_row = []
    
    # Initialize index for iterating through the input row
    i = 0
    
    # Iterate through the input row
    while i < width:
        # Get the color of the current pixel
        current_color = input_row[i]
        
        # Case 1: Background pixel
        if current_color == 0:
            output_row.append(0)
            i += 1 # Move to the next pixel
        # Case 2: Non-background pixel
        else:
            # Check if it's a 3-pixel block
            # Crucially, check bounds *before* accessing indices i+1 and i+2
            is_three_block = False
            if i + 2 < width: # Check if indices i+1 and i+2 are valid
                if input_row[i+1] == current_color and input_row[i+2] == current_color:
                    is_three_block = True
            
            # Subcase 2a: It's an existing 3-pixel block
            if is_three_block:
                # Append the block to the output
                output_row.extend([current_color, current_color, current_color])
                # Advance index past the block
                i += 3 
            # Subcase 2b: It's a single pixel (or start of shorter block) - expand it
            else:
                # Append the expanded block (3 pixels of current_color) to the output
                output_row.extend([current_color, current_color, current_color])
                # Advance index by 1 (only consuming the original single pixel)
                i += 1 
                
    # Return the output row wrapped in a list to match grid format
    return [output_row]
