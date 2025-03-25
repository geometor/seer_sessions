"""
1.  **Identify Horizontal Pairs:** Find all pairs of horizontally adjacent pixels that have different colors.
2.  **Create Green Bars:** For each identified horizontal pair, create a 2x1 block of green (color 3) pixels directly below it. The top of the green block should start one row below the identified pair.
3.  **Fill Single Row Gaps:** If there are two "horizontal pairs" stacked vertically with a gap of *exactly* one row between them, fill that gap row with green pixels, aligned horizontally with the pairs.
"""

import numpy as np

def find_horizontal_pairs(grid):
    """Finds pairs of horizontally adjacent pixels with different colors."""
    pairs = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 1):
            if grid[r, c] != grid[r, c + 1] and grid[r,c] != 0 and grid[r,c+1] != 0:
                pairs.append(((r, c), (r, c + 1)))
    return pairs

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find horizontal pairs
    pairs = find_horizontal_pairs(input_grid)

    # Create green bars below each pair
    for pair in pairs:
        (r1, c1), (r2, c2) = pair
        if r1 + 1 < rows:  # Check bounds
            output_grid[r1 + 1, c1] = 3
            output_grid[r1 + 1, c2] = 3
        if r1 + 2 < rows:
            output_grid[r1 + 2, c1] = 3
            output_grid[r1 + 2, c2] = 3
    
    # Fill single-row gaps between vertically stacked pairs.
    for pair1 in pairs:
        (r11, c11), (r12, c12) = pair1
        for pair2 in pairs:
            (r21, c21), (r22, c22) = pair2
            if r21 == r11 + 2: #check if there is a one row gap.
                if (c11 == c21 and c12==c22):
                  output_grid[r11+1,c11] = 3
                  output_grid[r11+1,c12] = 3

    return output_grid