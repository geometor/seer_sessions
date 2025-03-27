import numpy as np

"""
Transformation Rule:

1.  Identify the two non-white pixels in the input grid. These 'endpoints' are assumed to be on the same row.
2.  Determine the left endpoint (smaller column index) and the right endpoint (larger column index), noting their colors and shared row index.
3.  Calculate the column index of the pixel exactly halfway between the endpoints horizontally: `midpoint_col = floor((col_left + col_right) / 2)`.
4.  Fill the pixels on the shared row between the left endpoint (exclusive) and the midpoint column (exclusive) with the color of the left endpoint.
5.  Set the pixel at the midpoint column on the shared row to gray (5).
6.  Fill the pixels on the shared row between the midpoint column (exclusive) and the right endpoint (exclusive) with the color of the right endpoint.
7.  All other pixels remain unchanged from the input grid.
"""

def find_non_white_pixels(grid):
    """Finds all non-white pixels and returns their coordinates and colors."""
    non_white_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white_pixels.append(((r, c), grid[r, c]))
    return non_white_pixels

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Finds two endpoint pixels on the same row, calculates the midpoint,
    and fills the space between them based on their colors, placing gray at the midpoint.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the non-white pixels (endpoints)
    endpoints_info = find_non_white_pixels(input_grid)
    
    # Expecting exactly two non-white pixels based on examples
    if len(endpoints_info) != 2:
        # If not exactly two, return the original grid or handle error
        # Based on the examples, we assume there are always two.
        return output_grid 
        
    (pos1, color1), (pos2, color2) = endpoints_info
    r1, c1 = pos1
    r2, c2 = pos2

    # Verify they are on the same row (as per perception)
    if r1 != r2:
        # If not on the same row, return original grid or handle error
        return output_grid
        
    shared_row = r1
    
    # Determine left and right endpoints
    if c1 < c2:
        c_left, color_left = c1, color1
        c_right, color_right = c2, color2
    else:
        c_left, color_left = c2, color2
        c_right, color_right = c1, color1
        
    # Calculate the midpoint column index
    # Use integer division // which effectively floors the result
    midpoint_col = (c_left + c_right) // 2
    
    # Fill the segment left of the midpoint
    for col in range(c_left + 1, midpoint_col):
        output_grid[shared_row, col] = color_left
        
    # Set the midpoint pixel to gray (5)
    # Check if there is a gap to fill (i.e., c_right > c_left + 1)
    if c_right > c_left + 1:
         output_grid[shared_row, midpoint_col] = 5
    
    # Fill the segment right of the midpoint
    for col in range(midpoint_col + 1, c_right):
        output_grid[shared_row, col] = color_right
        
    return output_grid
