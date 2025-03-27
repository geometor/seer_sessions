"""
Identify the two distinct non-white colors present in the input grid. 
Select the color with the larger numerical value.
Create a 2x2 output grid filled entirely with the selected color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Find the two non-white colors, select the one with the higher numerical index,
    and output a 2x2 grid filled with that color.
    """
    # Convert the input list of lists to a numpy array for easier processing
    grid = np.array(input_grid, dtype=int)

    # Find all unique non-zero values (colors) in the grid
    unique_colors = np.unique(grid)
    non_white_colors = unique_colors[unique_colors != 0]

    # Check if there are exactly two non-white colors (as observed in examples)
    if len(non_white_colors) != 2:
        # This case isn't explicitly handled by the examples, but we can default
        # or raise an error. Let's choose the max if available, or return empty/error.
        # For now, let's assume the pattern holds and find the maximum non-white color.
        if len(non_white_colors) > 0:
             winning_color = np.max(non_white_colors)
        else:
            # Handle the case where there are no non-white colors, maybe return an empty grid or 0s?
            # Let's return a 2x2 grid of white (0) as a fallback.
            winning_color = 0
    else:
        # Find the maximum of the two non-white colors
        winning_color = np.max(non_white_colors)

    # Create a 2x2 output grid
    output_grid = np.full((2, 2), winning_color, dtype=int)

    # Return the output grid (implicitly converted back to list of lists by the framework if needed)
    return output_grid.tolist()