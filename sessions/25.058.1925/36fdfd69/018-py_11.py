"""
The transformation rule is as follows:

1.  **Identify Horizontally Adjacent Red Pairs:** Scan the input grid to find pairs of horizontally adjacent red (2) pixels.
2.  **Place Yellow to the Right:** For each horizontally adjacent red pair, place a yellow (4) pixel immediately to the right of the rightmost red pixel in the output grid.
3.  **Preserve Other Pixels:** All other pixels from the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_horizontal_red_pairs(grid):
    """Finds horizontally adjacent red pixels."""
    red_pairs = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1] - 1):
            if grid[r, c] == 2 and grid[r, c + 1] == 2:
                red_pairs.append(((r, c), (r, c + 1)))
    return red_pairs

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)  # Initialize with the input grid
    red_pairs = find_horizontal_red_pairs(input_grid)
    for pair in red_pairs:
        (_, c1), (_, c2) = pair
        # Place yellow pixel to the right of the pair
        if c2 + 1 < output_grid.shape[1]:
           output_grid[c1,c2+1] = 4
        

    return output_grid