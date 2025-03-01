"""
The transformation rule depends on the input grid. If all values in the input grid are the same, the output grid is filled with '4' (yellow). If the input grid contains values '1' and '0', replace '1' with '2' (red). Otherwise, apply the original rule: a repeating pattern of '4, 8, 3', where the specific value at any position (i, j) is determined by (i + j) mod 3, indexing into the pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on different rules depending on its content.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    unique_values = np.unique(input_grid)
    
    # If all values are the same, fill the output grid with 4.
    if np.all(input_grid == input_grid.flatten()[0]):
        output_grid[:] = 4
    # if the unique colors are 1 and 0, replace 1 with 2, leave zero as is
    elif set(unique_values) == {0, 1}:
        output_grid[input_grid == 1] = 2
        output_grid[input_grid == 0] = 0
    # Otherwise, use (i + j) % 3 with the pattern [4, 8, 3].
    else:
        pattern = [4, 8, 3]
        for i in range(rows):
            for j in range(cols):
                output_grid[i, j] = pattern[(i + j) % len(pattern)]
    return output_grid.tolist()