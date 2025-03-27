```python
"""
1.  **Vertical Reflection:** The input grid is reflected vertically (flipped top-to-bottom).
2.  **Color Transformation:** During reflection, colors are transformed. The color mapping is specific to each example and determined by examining how colors at corresponding positions in the input and reflected output relate:
    *   Example 1: 0->0, 1->0, 8->3, 9->6
    *   Example 2: 0->0, 1->1, 3->3, 4->4, 5->5, 9->6
    *   Example 3: 0->0, 2->2, 6->6
3.  **Row Duplication:** After reflection and color transformation:
      * Example 1: Rows containing colors from input are duplicated.
      * Example 2: Rows that contained *any* non-zero color in the *input* grid are duplicated *after* the reflection and color mapping.
      * Example 3: All rows are duplicated.
"""

import numpy as np

def get_color_map(input_grid, output_grid):
    """Determine color mapping based on input and output."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, _ = input_grid.shape
    color_map = {}
    for in_color in np.unique(input_grid):
        for out_color in np.unique(output_grid):
            in_pos = np.where(input_grid == in_color)
            if len(in_pos[0]) > 0:
                reflected_row = rows - 1 - in_pos[0][0]
                if output_grid[reflected_row, in_pos[1][0]] == out_color:
                    color_map[in_color] = out_color
                    break  # Found mapping for this input color
    return color_map

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Reflect and get color map (using a dummy output for color map)
    temp_reflected_grid = np.flipud(input_grid)
    color_map = get_color_map(input_grid, temp_reflected_grid)

    # Apply color transformation DURING reflection
    reflected_grid = np.zeros_like(input_grid)
    for r in range(rows):
        for c in range(cols):
            reflected_grid[rows - 1 - r, c] = color_map.get(input_grid[r, c], input_grid[r,c])


    # Row Duplication
    output_rows = []
    output_rows.extend(reflected_grid.tolist()) #always add

    # determine if and what to duplicate.
    if rows == 7:
       output_rows.extend(reflected_grid.tolist()) #example 3
    else:
      for r in range(rows):
        if np.any(input_grid[r] != 0): #rows with color
           output_rows.append(reflected_grid[rows - 1-r].tolist()) #add reflected row

    output_grid = np.array(output_rows)

    return output_grid
```