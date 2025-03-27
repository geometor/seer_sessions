```python
"""
1.  Identify the single non-zero color present in the input grid.
2.  Create an output grid of the same dimensions as the input grid.
3.  Fill the last row of output grid with the identified non-zero color.
4.  Fill the last column of output grid with the identified non-zero color.
5.  Iterate on input grid, if any color other than background ('0'), set corresponding output pixel to same color.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid of the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    
    # Identify the single non-zero color present in the input grid.
    non_zero_colors = np.unique(input_grid[input_grid != 0])
    if len(non_zero_colors) > 0:
        non_zero_color = non_zero_colors[0]
    else:
        non_zero_color = 0  # Default to 0 if no non-zero color is found

    # Fill the last row and last column with the non zero color.
    output_grid[-1, :] = non_zero_color
    output_grid[:, -1] = non_zero_color

    # Iterate on input grid and set the output.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i][j] != 0:
                output_grid[i][j] = input_grid[i][j]

    return output_grid
```