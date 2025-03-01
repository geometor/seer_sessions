# 0d3d703e • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Input:** A 3x3 grid where each cell contains a single-digit color code.
2.  **Transformation:** For each cell in the input grid, replace its value according to the following mapping:
    *   If the value is 9, change it to 8.
    *   If the value is 4, change it to 3.
    *   If the value is 2, change it to 6.
    *   Otherwise, leave unchanged // implicit rule
3.  **Output:** A 3x3 grid with the transformed cell values, maintaining the original grid structure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy to modify
    output_grid = np.copy(input_grid)

    # Define the color mapping
    color_map = {
        9: 8,
        4: 3,
        2: 6
    }

    # Iterate through each cell of the grid
    for row_index, row in enumerate(input_grid):
        for col_index, cell_value in enumerate(row):
            # Apply the color mapping if the value is in the map
            if cell_value in color_map:
                output_grid[row_index, col_index] = color_map[cell_value]

    return output_grid
```
