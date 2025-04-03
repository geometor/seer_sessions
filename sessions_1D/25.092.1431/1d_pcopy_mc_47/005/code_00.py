import numpy as np # Common library, although list operations suffice here

"""
Transforms a 1xN input grid based on sequences of colored pixels.

The transformation iterates through the input row pixel by pixel:
1. If a pixel is background (0), it's copied directly to the output, and the input index advances by 1.
2. If a non-background pixel (color C) is encountered:
   a. Three pixels of color C (C, C, C) are appended to the output.
   b. The input index is advanced by 3. This effectively treats every non-background pixel encountered as the start of a 3-pixel block in the output, consuming 3 positions from the input perspective, regardless of whether the following two input pixels were originally background or the same color.
The process continues until the input index reaches or exceeds the input width. The resulting output row can be longer than the input row.
"""

def transform(input_grid):
    """
    Applies the corrected transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): A 1xN grid.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Ensure input is a list of lists and extract the single row
    # Handle potential issues like numpy arrays or empty inputs
    if isinstance(input_grid, np.ndarray):
        # Convert numpy array to list of lists if necessary
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            input_row = input_grid.tolist()[0]
        else:
            # Handle unexpected numpy array shape or return empty
            return [[]] 
    elif isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list):
        input_row = input_grid[0]
    else:
        # Return empty grid for invalid input format
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
            # Append background pixel to output
            output_row.append(0)
            # Advance input index by 1
            i += 1 
        # Case 2: Non-background pixel
        else:
            # Append three pixels of the current color to the output
            output_row.extend([current_color, current_color, current_color])
            # Advance input index by 3 (consuming the space for the 3-block)
            # This handles both expansion of singles and preserves existing blocks implicitly
            i += 3 
                
    # Return the output row wrapped in a list to match grid format
    return [output_row]
