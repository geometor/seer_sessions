"""
1. Copy Base: Copy the two solid rows of gray (5) pixels from the input grid to the same positions in the output grid.

2. Replace and Expand:
    *   Iterate through the input grid.
    *   If a pixel is blue (1), change it to gray (5) in the output grid.
    *   If blue pixels are adjacent horizontally, vertically or diagonally, group them to create bigger gray shapes in corresponding locations of output

3. Remove: All blue pixels are removed or replaced.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid).astype(int)

    # Find the two rows of gray pixels (assuming they are always present and full rows)
    rows_with_gray = []
    for i, row in enumerate(input_grid):
        if np.all(row == 5):
            rows_with_gray.append(i)

    # Copy the gray rows to the output grid
    for row_index in rows_with_gray:
        output_grid[row_index, :] = 5
        
    # Iterate through the input grid and replace blue with gray
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 1:
                output_grid[i, j] = 5

    return output_grid