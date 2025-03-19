"""
The transformation rule is as follows:
1. Identify the top section: The top section consists of the first two rows of the input grid.
2. Preserve the top section: Copy the top section directly to the output grid.
3. Identify the repeating pattern: The first row of the input represents the colors to build a vertically repeating pattern.
4. Generate repeating pattern rows: Create new rows with the colors from the top row.
5. Fill the bottom section of output: Starting from the 3rd row, fill rows of output with the colors red, blue, and yellow repeated. The output has the same dimensions as the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify the repeating pattern from the first row
    repeating_pattern = input_grid[0]

    # Fill the bottom section of the output grid starting from the third row
    pattern_index = 0
    for i in range(2, rows):
        output_grid[i] = repeating_pattern[pattern_index % cols]
        pattern_index +=1

    return output_grid