# f2829549 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Column Selection:** From the input grid, select columns 3, 5 and 6 (remembering that columns and rows are zero indexed).

2.  **Color Replacement:** In the selected columns,
    *   Replace all instances of color 1 (blue) with color 3 (green).
    *   Replace all instances of color 5 (gray) with color 3 (green).
    *   Replace all instance of color 7 (orange) with color 0 (white)

3. **Output Formation:** Create a new output grid using only the modified selected columns. The dimensions of the output grid will be 4x3 (height x width).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_height, input_width = input_grid.shape
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Column Selection: Select columns 3, 5, and 6 (index 2, 4, and 5).
    selected_columns = [2, 4, 5]

    # Iterate through selected columns and copy/transform
    for j, col_index in enumerate(selected_columns):
        for i in range(output_height):
            # Color Replacement
            if input_grid[i, col_index] == 1:  # blue
                output_grid[i, j] = 3      # green
            elif input_grid[i, col_index] == 5:  # gray
                output_grid[i, j] = 3      # green
            elif input_grid[i,col_index] == 7: #orange
                output_grid[i,j] = 0      #white
            else:
                output_grid[i,j] = input_grid[i,col_index]


    return output_grid.tolist()
```
