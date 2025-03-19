# 4c4377d9 • 006 • refine_coder

---
```python
"""
The transformation rule observes the input grid and extracts the inner rectangle and its properties to reproduce in the output grid.
1. Identify the largest inner rectangle formed by colors different than the border.
2. Extract the subgrid that makes up the inner rectangle.
3. The subgrid is the output.
"""

import numpy as np

def find_inner_rectangle(grid):
    """
    Finds the largest inner rectangle in a grid.

    Args:
        grid (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (top, left, bottom, right) coordinates of the inner rectangle,
               or None if no inner rectangle is found.
    """
    rows, cols = grid.shape
    top, left, bottom, right = 0, 0, rows - 1, cols - 1

    # Find top boundary
    first_row_color = grid[0, 0]
    for i in range(rows):
        if not np.all(grid[i, :] == first_row_color):
            top = i
            break
    else:
        return None  # No inner rectangle found

    # Find bottom boundary
    last_row_color = grid[-1, 0]
    for i in range(rows - 1, -1, -1):
        if not np.all(grid[i, :] == last_row_color):
            bottom = i
            break

    # Find left boundary
    first_col_color = grid[0,0]
    for j in range(cols):
        if not np.all(grid[:, j] == first_col_color):
            left = j
            break

    # Find right boundary
    last_col_color = grid[0,-1]
    for j in range(cols - 1, -1, -1):
        if not np.all(grid[:, j] == last_col_color):
            right = j
            break
            
    #check if the colors in first and last columns/rows are the same
    if not (first_row_color == last_row_color and first_col_color == last_col_color):
        return None #not an inner rect

    return (top, left, bottom, right)

def transform(input_grid):
    """
    Transforms the input grid by extracting the inner rectangle.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid, which is the inner rectangle of the input.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Find the inner rectangle.
    inner_rectangle_coords = find_inner_rectangle(input_array)

    # If no inner rectangle is found, return an empty grid.
    if inner_rectangle_coords is None:
        return []

    # Extract the inner rectangle.
    top, left, bottom, right = inner_rectangle_coords
    output_array = input_array[top:bottom+1, left:right+1]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```
