"""
1.  **Examine Input:** Get the dimensions (rows and columns) of the input grid.
2.  **Calculate Output Dimensions:** The output grid dimensions are calculated by subtracting 1 from the number of rows and 2 from the number of columns.
3. **Create output:** create a new, blank output grid of the appropriate dimensions, filled with the background color (0).
4. **Return:** return the output grid.
"""

import numpy as np

def transform(input_grid):
    # Examine Input: Get dimensions
    input_rows, input_cols = np.array(input_grid).shape

    # Calculate Output Dimensions
    output_rows = input_rows - 1
    output_cols = input_cols - 2

    # Create output: Initialize with background color (0)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Return: output grid
    return output_grid