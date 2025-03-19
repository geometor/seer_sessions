"""
Copy input grid to the output grid. For every even row, change every even position gray cell into a green cell.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    Gray pixels at even indices within even rows are changed to green.
    """
    output_grid = np.copy(input_grid)  # Start with a copy of the input
    rows, cols = output_grid.shape

    for i in range(rows):
        for j in range(cols):
            # Conditional Replacement
            if output_grid[i, j] == 5:  # If the pixel is gray
                if i % 2 == 0 and (i * cols + j) % 2 == 0 : # check row index and overall index
                  output_grid[i, j] = 3  # Change to green

    return output_grid