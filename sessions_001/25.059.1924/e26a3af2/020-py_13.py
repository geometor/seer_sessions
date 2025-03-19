"""
The transformation identifies horizontal stripes of colors 3 (green), 7 (orange), 8 (azure), and 1 (blue) in the input.  The output grid consists entirely of repetitions of the identified stripes, maintaining the vertical order in which they first appear. The key is that only *one* color stripe is extracted from input, and the output is a solid block of the same color.
"""

import numpy as np

def get_horizontal_stripes(input_grid):
    """
    Identifies and returns the first horizontal stripe of specified colors (3, 7, 8, or 1).
    """
    rows, cols = input_grid.shape
    target_colors = [3, 7, 8, 1]
    stripes = []

    for r in range(rows):
        row_colors = []
        for c in range(cols):
            row_colors.append(input_grid[r, c])
        
        # Check if the entire row is the same color and is a target color
        if len(set(row_colors)) == 1 and row_colors[0] in target_colors:
            stripes.append((r, row_colors[0]))
    return stripes

def transform(input_grid):
    """
    Transforms the input grid based on identified horizontal stripes.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get horizontal stripes
    stripes = get_horizontal_stripes(input_grid)
    
    # reconstruct based on stripes
    stripe_index = 0
    
    for r in range(rows):
        if stripe_index < len(stripes):
            output_grid[r,:] = stripes[stripe_index][1]
            stripe_index = (stripe_index + 1) % len(stripes) # cycle through stripes
        else:
           # handle no more stripes - which means use the last stripe
           if stripes:  # Ensure stripes is not empty
               output_grid[r, :] = stripes[-1][1]
           else:
                pass

    return output_grid