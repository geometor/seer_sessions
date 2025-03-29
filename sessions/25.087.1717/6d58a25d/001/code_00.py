import numpy as np

"""
Transforms the input grid based on a 'plus' shape and scattered pixels.

1.  Identifies two non-white colors: one forming a 5-pixel 'plus' shape 
    (shape_color) around a central white pixel, and another scattered color 
    (filler_color).
2.  Locates the central white pixel (center_row, center_col) of the plus shape.
3.  Fills this central pixel with the filler_color.
4.  Draws two vertical lines downwards from two rows below the center, aligned 
    with the left and right arms of the plus shape (columns center_col - 1 and 
    center_col + 1), using the filler_color. These lines extend to the bottom 
    of the grid.
"""

def find_plus_center_and_colors(grid):
    """
    Finds the center of the plus shape, the shape color, and the filler color.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (shape_color, filler_color, center_row, center_col) or 
               (None, None, None, None) if not found.
    """
    rows, cols = grid.shape
    non_zero_colors = np.unique(grid[grid != 0])
    
    if len(non_zero_colors) != 2:
        # This specific task structure expects exactly two non-background colors
        return None, None, None, None 
        
    color1, color2 = non_zero_colors

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check if the current pixel is white (0)
            if grid[r, c] == 0:
                # Check neighbors for the plus shape pattern
                up = grid[r - 1, c]
                down = grid[r + 1, c]
                left = grid[r, c - 1]
                right = grid[r, c + 1]
                
                # Check if all neighbours are the same non-zero color
                if up != 0 and up == down == left == right:
                    shape_color = up
                    # Determine filler color
                    filler_color = color1 if shape_color == color2 else color2
                    return shape_color, filler_color, r, c
                    
    return None, None, None, None # Should not happen based on examples


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Find the plus shape characteristics
    shape_color, filler_color, center_row, center_col = find_plus_center_and_colors(input_grid)

    if center_row is None:
        # If no plus shape found, return the original grid (or handle error)
        # Based on task description, a plus shape should always be present.
        return np.copy(input_grid) 

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Fill the center of the plus shape
    output_grid[center_row, center_col] = filler_color

    # Draw the two vertical lines below the plus shape
    # Start from 2 rows below the center
    start_row = center_row + 2
    left_col = center_col - 1
    right_col = center_col + 1

    # Ensure columns are within bounds (though unlikely needed based on shape)
    if 0 <= left_col < cols and 0 <= right_col < cols:
        for r in range(start_row, rows):
            output_grid[r, left_col] = filler_color
            output_grid[r, right_col] = filler_color

    return output_grid