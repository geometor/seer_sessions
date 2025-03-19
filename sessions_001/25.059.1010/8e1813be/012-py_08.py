"""
Identifies the rightmost column containing a blue (1), red (2), or yellow (4) pixel.
From these columns, it constructs a 3x3 grid where each row is a copy of those color values.
If fewer than 3 such values, it fills with background (0). If more than 3, uses the first 3.
"""

import numpy as np

def get_rightmost_target_colors(input_grid):
    """
    Finds the rightmost occurrence of each target color (1, 2, and 4) in the input grid.
    Returns a list of these color values, maintaining the order [blue, red, yellow].
    """
    target_colors = [1, 2, 4]
    rightmost_values = []

    for color in target_colors:
        rightmost_col_with_color = -1
        for j in range(input_grid.shape[1]):  # Iterate through columns
            for i in range(input_grid.shape[0]):
                if input_grid[i, j] == color:
                    rightmost_col_with_color = j  # Update to use rightmost

        if rightmost_col_with_color != -1:
            for i in range(input_grid.shape[0]):
               if input_grid[i,rightmost_col_with_color] == color: #find first occurence
                   rightmost_values.append(color)
                   break # stop searching rows
        
    return rightmost_values

def transform(input_grid):
    # Find rightmost values of target colors
    target_values = get_rightmost_target_colors(input_grid)

    # Handle edge case: fewer than 3 target values
    while len(target_values) < 3:
        target_values.append(0)  # Append background (0) if needed

    # Handle edge case: more than 3 target values
    if len(target_values) > 3:
        target_values = target_values[:3]  # Keep only the first 3

    # Construct the 3x3 output grid
    output_grid = np.array([target_values, target_values, target_values])

    return output_grid