```python
"""
Transforms an input grid by swapping the colors of the border and the inner rectangle.
The border color of the input becomes the inner rectangle color of the output, and the
inner rectangle color of the input becomes the border color of the output.
"""

import numpy as np

def get_border_color(grid):
    """Gets the border color of the grid."""
    return grid[0, 0]

def find_inner_rectangle(grid):
    """Finds the inner rectangle's color, start row, start col, height, and width."""
    grid = np.array(grid)
    border_color = get_border_color(grid)
    rows, cols = grid.shape
    
    # Find the first pixel that is not the border color
    start_row, start_col = -1, -1
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r, c] != border_color:
                start_row, start_col = r, c
                break
        if start_row != -1:
            break
            
    if start_row == -1: # No inner rectangle found
        return None, 0, 0, 0, 0

    inner_color = grid[start_row, start_col]
    
    # Determine height
    height = 0
    for r in range(start_row, rows - 1):
        if grid[r, start_col] == inner_color:
            height += 1
        else:
            break

    # Determine width
    width = 0
    for c in range(start_col, cols - 1):
        if grid[start_row, c] == inner_color:
            width += 1
        else:
            break

    return inner_color, start_row, start_col, height, width

def transform(input_grid):
    """Transforms the input grid by swapping border and inner rectangle colors."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get the border color of the input grid.
    input_border_color = get_border_color(input_grid)

    # Find the inner rectangle
    inner_color, start_row, start_col, height, width = find_inner_rectangle(input_grid)

    if inner_color is None:  # Handle cases with no inner rectangle (all same color)
        return output_grid.tolist()

    # Fill the output grid's border with the inner rectangle color.
    output_grid[0, :] = inner_color
    output_grid[-1, :] = inner_color
    output_grid[:, 0] = inner_color
    output_grid[:, -1] = inner_color

    # Fill the inner rectangle of the output grid with the input border color.
    output_grid[start_row:start_row+height, start_col:start_col+width] = input_border_color
    
    return output_grid.tolist()
```