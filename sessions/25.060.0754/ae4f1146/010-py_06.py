"""
The transformation rule can be described as follows:

1.  **Divide**: Divide the input 9x9 grid into nine 3x3 non-overlapping subgrids.
2.  **Reduce**: For each 3x3 subgrid in the input:
    *   Iterate through each cell in the subgrid.
    *    If all cells in the region are background (0/white) the output is also background (0/white)
    *   If any value other than background(0/white) is present, evaluate the non-zero values.
3.  **Output**: The result of each subgrid represents a single cell in the 3x3 output grid in the corresponding location.
   *  If at any cell in a region contains a blue (1), the output cell is blue (1).
   *  If there are not blues(1) and any cell in the region is azure (8), then the output cell is azure (8).

In essence, the output grid is a 3x3 "summary" of the input grid, where each output cell represents a 3x3 block of the input. Prioritizing 1s and 8s, while filtering out any surrounding background.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 9x9 input grid into a 3x3 output grid based on the described rule."""

    input_array = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize the output grid with zeros

    # Iterate through the 3x3 subgrids
    for i in range(3):
        for j in range(3):
            # Extract the 3x3 subgrid
            subgrid = input_array[i*3:(i+1)*3, j*3:(j+1)*3]

            # Apply the reduction rule
            if np.any(subgrid == 1):
                output_grid[i, j] = 1  # Blue (1) takes precedence
            elif np.any(subgrid == 8):
                output_grid[i, j] = 8  # Azure (8) if no Blue (1)
            # else: keep the default 0.

    return output_grid.tolist()