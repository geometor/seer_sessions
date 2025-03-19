# ba97ae07 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies a vertical and a horizontal line within the input grid.
It then replaces the color of the cell where these lines intersect with the color of the vertical line, but only within the horizontal line.
"""

import numpy as np

def find_line(grid, direction):
    """
    Finds a horizontal or vertical line in the grid.
    direction: 'horizontal' or 'vertical'
    """
    if direction == 'horizontal':
        for r_idx, row in enumerate(grid):
            unique_colors = np.unique(row)
            for color in unique_colors:
                if color != 0 and np.all(row[row != 0] == color):
                    return r_idx, color
    elif direction == 'vertical':
        for c_idx in range(grid.shape[1]):
            col = grid[:, c_idx]
            unique_colors = np.unique(col)
            for color in unique_colors:
                if color != 0 and np.all(col[col != 0] == color):
                    return c_idx, color
    return None, None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the horizontal and vertical lines
    h_row_idx, h_color = find_line(input_grid, 'horizontal')
    v_col_idx, v_color = find_line(input_grid, 'vertical')

    # check if h_row_idx and v_col_idx exist before proceeding.
    if h_row_idx is not None and v_col_idx is not None:      
        # Apply transformation: replace color at intersection within horizontal line
        output_grid[h_row_idx, v_col_idx] = v_color

    return output_grid
```
