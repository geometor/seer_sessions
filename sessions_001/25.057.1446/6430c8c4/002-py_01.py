"""
1.  **Identify Region:** Locate the 4x4 subgrid at the top-left corner of the input grid.
2.  **Extract Subgrid**: Create a new, empty 4x4 grid.
3.  **Map Colors:** For each cell within the located 4x4 subgrid in the *input* grid:
    *   If the cell's value is 7 (orange), set the corresponding cell in the *output* grid to 3 (green).
    *   Otherwise, set the corresponding cell in the *output* grid to 0 (white).
4. **Return Output Grid**: Return the resulting 4x4 output grid
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid to an output grid based on the described rules."""

    # Initialize output_grid as a 4x4 numpy array filled with 0s (white)
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the 4x4 subgrid at the top-left corner of the input grid
    for i in range(4):
        for j in range(4):
            # Map colors based on the input grid's values
            if input_grid[i, j] == 7:  # If the value is 7 (orange)
                output_grid[i, j] = 3  # Set the corresponding cell to 3 (green)
            else:
                output_grid[i, j] = 0  # Otherwise, set to 0 (white)

    return output_grid