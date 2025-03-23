```python
"""
1.  **Identify Target Color:** Examine the input grid and identify the single non-black color present.
2.  **Count Non-Black Pixels:** Count how often this color appears in the input.
3. **Determine size:** Inspect the input grid and count the largest grouping of the target color either in a row or column. This is length of a dimension in the output grid.
4.  **Construct Output Grid:** Create a new square grid, where each dimension is equal to calculated value from step 3. Fill every cell of this new grid with the target color identified in step 1.
"""

import numpy as np

def get_target_color(grid):
    # Find unique colors in the grid, excluding black (0)
    unique_colors = np.unique(grid)
    target_colors = unique_colors[unique_colors != 0]
    # Return the first non-black color, assumes there's only one
    if len(target_colors) > 0:
       return target_colors[0]
    else:
        return 0

def get_max_dimension(grid, target_color):
    max_row = 0
    for row in grid:
        count = np.count_nonzero(row == target_color)
        if count > max_row:
           max_row = count
    max_col = 0
    for col in grid.T:
        count = np.count_nonzero(col == target_color)
        if count > max_col:
           max_col = count

    return max(max_row, max_col)
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Target Color
    target_color = get_target_color(input_grid)
    if target_color == 0: return []

    #2. & 3. Count and determine output grid size.
    output_size = get_max_dimension(input_grid, target_color)


    # 4. Construct Output Grid
    output_grid = np.full((output_size, output_size), target_color)

    return output_grid.tolist()
```