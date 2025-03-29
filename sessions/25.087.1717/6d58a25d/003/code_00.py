import numpy as np

"""
Transforms the input grid based on identifying a specific pattern and drawing lines.

The transformation rule involves these steps:
1.  Identify two distinct non-white colors in the grid. One color ('shape_color') 
    forms a specific pattern around a central white pixel, and the other 
    ('filler_color') is scattered elsewhere.
2.  Locate the central white pixel (center_row, center_col) which has the 
    'shape_color' directly above it, to its left, and to its right. 
    Specifically, find (r, c) such that grid[r, c] == 0 and 
    grid[r-1, c] == grid[r, c-1] == grid[r, c+1] == shape_color.
3.  Change the color of the central pixel (center_row, center_col) in the output 
    grid to the 'filler_color'.
4.  Starting two rows below the central pixel (from row center_row + 2), draw two 
    vertical lines downwards to the bottom edge of the grid. These lines use the 
    'filler_color'.
5.  The columns for these vertical lines are determined by the columns immediately 
    to the left and right of the central pixel's column (center_col - 1 and 
    center_col + 1).
6.  All other pixels retain their original colors from the input grid.
"""

def find_pattern_center_and_colors(grid):
    """
    Finds the center of the pattern, the shape color, and the filler color.

    The pattern is a white pixel (r, c) where the pixels at (r-1, c), 
    (r, c-1), and (r, c+1) are all the same non-white color (shape_color).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (shape_color, filler_color, center_row, center_col) or 
               (None, None, None, None) if the pattern is not found or if there 
               are not exactly two non-white colors.
    """
    rows, cols = grid.shape
    # Find all unique non-white colors
    non_white_colors = np.unique(grid[grid != 0])
    
    # The task structure expects exactly two non-white colors
    if len(non_white_colors) != 2:
        return None, None, None, None 
        
    color1, color2 = non_white_colors

    # Iterate through possible center pixels (avoiding edges)
    for r in range(1, rows): # Need to check r-1
        for c in range(1, cols - 1): # Need to check c-1 and c+1
            # Check if the current pixel is white (0)
            if grid[r, c] == 0:
                # Check neighbors for the specific pattern
                up = grid[r - 1, c]
                left = grid[r, c - 1]
                right = grid[r, c + 1]
                
                # Check if up, left, right are the same non-white color
                if up != 0 and up == left == right:
                    shape_color = up
                    # Determine the filler color (the other non-white color)
                    filler_color = color1 if shape_color == color2 else color2
                    # Pattern found, return the details
                    return shape_color, filler_color, r, c
                    
    # Pattern not found
    return None, None, None, None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Find the pattern characteristics
    shape_color, filler_color, center_row, center_col = find_pattern_center_and_colors(input_grid)

    # If the required pattern wasn't found, return a copy of the input grid.
    # Based on the task examples, the pattern should always be present.
    if center_row is None:
        return np.copy(input_grid) 

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # --- Apply transformations ---

    # 1. Fill the center of the pattern with the filler_color
    output_grid[center_row, center_col] = filler_color

    # 2. Draw the two vertical lines below the pattern
    # Determine starting row (2 rows below center) and column positions
    start_row = center_row + 2
    left_col = center_col - 1
    right_col = center_col + 1

    # Ensure the calculated columns are within the grid boundaries
    # (This check might be redundant if the pattern is guaranteed not to be at the edge)
    if 0 <= left_col < cols and 0 <= right_col < cols:
        # Iterate from the start row down to the bottom of the grid
        for r in range(start_row, rows):
            # Draw pixels for both lines using the filler_color
            output_grid[r, left_col] = filler_color
            output_grid[r, right_col] = filler_color

    return output_grid