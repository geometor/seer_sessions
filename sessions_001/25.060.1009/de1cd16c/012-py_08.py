"""
1. Divide the input grid into four equal quadrants.
2. Determine the dominant color in the bottom-right quadrant.
3. Output the dominant color.
"""

import numpy as np
from collections import Counter

def get_quadrant(grid, quadrant_name):
    """Helper function to extract a specific quadrant from a grid."""
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant_name == "top_left":
        return grid[:mid_row, :mid_col]
    elif quadrant_name == "top_right":
        return grid[:mid_row, mid_col:]
    elif quadrant_name == "bottom_left":
        return grid[mid_row:, :mid_col]
    elif quadrant_name == "bottom_right":
        return grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant name")

def find_dominant_color(grid):
    """Helper function to find the most frequent color in a grid."""
    counts = Counter(grid.flatten())
    return counts.most_common(1)[0][0]

def transform(input_grid):
    """
    Identifies the dominant color in the bottom-right quadrant of the input grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Get the bottom-right quadrant
    bottom_right_quadrant = get_quadrant(input_grid, "bottom_right")

    # Find the dominant color in the bottom-right quadrant
    dominant_color = find_dominant_color(bottom_right_quadrant)
    
    # initialize output_grid to single value of dominant_color
    output_grid = np.array([[dominant_color]])

    return output_grid