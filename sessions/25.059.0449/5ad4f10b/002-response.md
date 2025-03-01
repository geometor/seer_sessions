# 5ad4f10b • 002 • example_3 • investigate_coder

---
```python
"""
The program extracts distinct colors from the input grid and places them into a 3x3 grid, roughly preserving their relative positions. The input grid is conceptually divided into nine equal sections, and the most prominent non-zero color in each section is mapped to the corresponding cell in the 3x3 output grid.
"""

import numpy as np

def get_sector_color(input_grid, row_start, row_end, col_start, col_end):
    # Extract the sector from the input grid
    sector = input_grid[row_start:row_end, col_start:col_end]
    # Find unique colors in the sector, excluding 0 (background)
    unique_colors = np.unique(sector)
    unique_colors = unique_colors[unique_colors != 0]
   
    if len(unique_colors) > 0:
        # Return the first non-zero color encountered
        return unique_colors[0]
    else:
        return 0 # Return background if only 0 is present.

def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid, preserving the relative
    positions of non-zero colored pixels.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Calculate sector boundaries
    row_step = rows // 3
    col_step = cols // 3
    
    # Iterate through each sector of output grid
    for i in range(3):
        for j in range(3):
            # Define boundaries of the corresponding input sector.  Handle
            # boundary conditions to cover the entire input
            row_start = i * row_step
            row_end = (i + 1) * row_step if i < 2 else rows
            col_start = j * col_step
            col_end = (j+1) * col_step if j < 2 else cols

            #apply color of the sector to the output grid
            output_grid[i, j] = get_sector_color(input_grid, row_start, row_end, col_start, col_end)

    return output_grid
```
