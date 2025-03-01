# 8eb1be9a • 010 • example_2 • investigate_coder

---
```python
"""
The transformation identifies a central horizontal band of red pixels in the input grid. 
It then extracts the alternating pattern of red and white pixels within this band (excluding the solid red lines). 
This pattern is replicated vertically, both upwards and downwards, to fill the entire output grid, while the fully red rows are preserved.
"""

import numpy as np

def find_red_band_rows(grid):
    """Finds the indices of rows that form the central red band."""
    red_rows = []
    for i, row in enumerate(grid):
        # Check if the row is mostly red (allowing for interspersed white pixels)
        if np.sum(row == 2) > grid.shape[1] / 2:  # At least half are red
            red_rows.append(i)
    return red_rows

def get_pattern(row):
    """Extracts the alternating red/white pattern from a single row."""
    return row

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the central red band rows.
    red_band_rows = find_red_band_rows(input_grid)
    
    # Separate fully red band and other rows
    fully_red_rows = []
    pattern_rows = []
    for row_index in red_band_rows:
        if np.all(input_grid[row_index] == 2):
            fully_red_rows.append(row_index)
        else:
            pattern_rows.append(row_index)


    # 2 & 3. Replicate and apply the pattern
    if pattern_rows:  # check to ensure the pattern rows are not empty.
        pattern = get_pattern(input_grid[pattern_rows[0]])

        row_idx = 0
        for i in range(height):
            if i in fully_red_rows:
                output_grid[i, :] = 2
            else:
                output_grid[i, :] = pattern
            

    return output_grid.tolist()
```
