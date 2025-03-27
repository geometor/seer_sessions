```python
"""
Iterates through each cell of the input grid. If the color is 1 (blue), 2 (red), 3 (green), or 8 (azure), 
it replaces the cell's value in the output grid with 5 (gray). Otherwise the input cell color is copied to the
output grid. Returns the modified grid as the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Check the color value of the cell
            if input_grid[i, j] in [1, 2, 3, 8]:
                # Replace the cell's value in the output grid with 5 (gray)
                output_grid[i, j] = 5
            # Else, the color remains the same (copy performed during initialization)

    # Return the modified grid as the output
    return output_grid
```
