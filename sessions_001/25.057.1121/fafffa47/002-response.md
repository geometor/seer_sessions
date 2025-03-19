# fafffa47 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Target Object:** Locate the contiguous region of pixels in the top-left corner of the input grid.
2.  **Determine Output Size**: The output size will be a subgrid of the input, that matches the size of this object.
3.  **Translate Color**: Map the color of the target object to the color red (2).
4.  **Construct Output:** Create a new grid with size set in (2). Fill any cell that corresponds with the target object with color red (2). Fill all remaining cells in with white (0).
"""

import numpy as np

def find_top_left_object(grid):
    # Find the top-left non-zero pixel
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                top_left_color = grid[r, c]
                top_left_coord = (r,c)
                return top_left_coord, top_left_color
    return None, None

def get_object_bounds(grid, start_row, start_col, color):
    """Gets the bounding box of a contiguous object."""
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    visited = set()
    stack = [(start_row, start_col)]

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
            min_row = min(min_row, r)
            max_row = max(max_row, r)
            min_col = min(min_col, c)
            max_col = max(max_col, c)

            # Add adjacent cells to the stack
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))
    return min_row, max_row, min_col, max_col



def transform(input_grid):
    # Find the top-left object and its color
    top_left_coord, top_left_color = find_top_left_object(input_grid)

    if top_left_coord is None:
        return np.zeros_like(input_grid)

    start_row, start_col = top_left_coord

    #get object bounds
    min_row, max_row, min_col, max_col = get_object_bounds(input_grid, start_row, start_col, top_left_color)

    # Determine output grid size
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    #fill in the output grid with the object, mapped to red
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
          if input_grid[r,c] == top_left_color:
            output_grid[r-min_row, c-min_col] = 2

    return output_grid
```
