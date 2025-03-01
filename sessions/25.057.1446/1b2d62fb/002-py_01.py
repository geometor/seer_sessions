"""
1.  **Extract Subgrid:** From the input grid, extract a 3-column wide subgrid. The subgrid starts from the 3rd column (index 2) and end at column 5 (index 4) of the input grid.
2.  **Replace Color:** Within this subgrid, locate all pixels with the color blue (value 1). Replace these pixels with the color azure (value 8).
3. **Finalize:** In the subgrid, modify row 3 to set value to 0, except any pixels of color 8.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Extract Subgrid
    output_grid = input_grid[:, 2:5]

    # 2. Replace Color
    output_grid = np.where(output_grid == 1, 8, output_grid)

    # 3. Finalize (modify row 3, setting non-8 values to 0)
    
    for i in range(output_grid.shape[1]):
        if output_grid[3,i] != 8:
            output_grid[3,i] = 0

    return output_grid