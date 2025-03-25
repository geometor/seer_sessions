"""
1.  **Input:** A 30x30 grid (the `input_grid`).
2.  **Divide:** Divide the `input_grid` into non-overlapping 3x3 `block`s.
3.  **Analyze:** For each `block`:
    *   Find the most frequent color, *excluding* white (color 1).
    *   If a block consists *only* of white pixels, then the most frequent color *is* white.
4.  **Construct Output:** Create a new grid (the `output_grid`) where each cell corresponds to a 3x3 block in the input grid.
     - the output grid dimensions are equal to the input_grid dimension divided by three, rounded up to nearest integer.
    *   The value of each cell in the `output_grid` is the most frequent color (determined in step 3) of the corresponding 3x3 `block` in the `input_grid`.
    * Fill the output grid in a top-to-bottom, left-to-right order (row-major order).
"""

import numpy as np
from collections import Counter
import math

def get_most_frequent_color(block):
    """Finds the most frequent color in a block, excluding 1s unless the block only contains 1s."""
    counts = Counter(block.flatten())
    if 1 in counts and len(counts) > 1:
        del counts[1]
    if not counts:
        return 1  # Handle cases with no colors (empty block, which shouldn't happen but good to be safe)
    most_common = counts.most_common(1)
    return most_common[0][0]

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = math.ceil(rows / 3)
    output_cols = math.ceil(cols / 3)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)


    # Iterate through 3x3 blocks
    for i in range(0, rows, 3):
        for j in range(0, cols, 3):
            block = input_grid[i:min(i+3, rows), j:min(j+3, cols)] # min handles edge cases
            # find most frequent color
            most_frequent = get_most_frequent_color(block)
            # output the most frequent into output grid
            output_row = i // 3
            output_col = j // 3
            output_grid[output_row, output_col] = most_frequent

    return output_grid.tolist()