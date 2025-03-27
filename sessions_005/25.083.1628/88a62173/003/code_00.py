"""
Extracts 2x2 sections from the top-left and bottom-right corners of the input grid (excluding a center row of zeros if present), combines them into a 4x2 intermediate array, rotates the combined array 90 degrees clockwise, and returns the result as a 2x2 output grid.
"""

import numpy as np

def get_top_left_corner(grid):
    """Extracts the top-left 2x2 corner, skipping the middle zero row if present."""
    rows, cols = grid.shape
    
    if rows % 2 == 1:  # Odd number of rows, skip the central row
        top_rows = grid[:rows//2, :2] # up to center row, first two columns
    else:  # Even number of rows, no skipping required, though not seen in training.
        top_rows = grid[:2,:2]
        
    return top_rows
    
def get_bottom_right_corner(grid):
    """Extract the bottom-right 2x2 corner, skipping the middle zero row if present."""
    rows, cols = grid.shape
    
    if rows % 2 == 1:
        bottom_rows = grid[rows//2 + 1:, -2:]  # Skip center row
    else:
        bottom_rows = grid[-2:, -2:]
    return bottom_rows


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    grid = np.array(input_grid)
    rows, cols = grid.shape
    
    # Get top-left corner pixels
    top_left = get_top_left_corner(grid)
    
    # Get bottom-right corner pixels.
    bottom_right = get_bottom_right_corner(grid)

    # Combine the two 2x2 corners into a single 4x2 array
    combined = np.concatenate((top_left, bottom_right), axis=0)


    # Rotate the combined grid 90 degrees clockwise.
    rotated_grid = np.rot90(combined, k=-1)

    return rotated_grid.tolist()