"""
The transformation rule involves identifying horizontal stripes of colors 3 (green), 7 (orange), 8 (azure), and 1 (blue) in the input grid and replicating them across the entire output grid. The key is to identify *any* horizontal stripe of these colors, regardless of its length (it just needs to be at least length 1). The output grid is then filled entirely with repetitions of these stripes, maintaining their original order.
"""

import numpy as np

def get_horizontal_stripes(input_grid):
    """
    Identifies and returns horizontal stripes of specified colors.
    """
    rows, cols = input_grid.shape
    target_colors = [3, 7, 8, 1]
    stripes = []

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] in target_colors:
                stripes.append((r, input_grid[r,c]))
                break # only the first occurence on a line
    return stripes
                

def transform(input_grid):
    """
    Transforms the input grid by replicating identified horizontal stripes of specific colors (3, 7, 8, and 1)
    across the entire output grid.
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
            stripe_index += 1
        else:
            # handle no more stripes
            pass
    return output_grid