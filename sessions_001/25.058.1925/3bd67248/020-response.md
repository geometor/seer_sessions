# 3bd67248 • 020 • refine_coder

---
```python
"""
1.  **Find Leftmost Azure Column:** Scan the input grid to find the leftmost column consisting entirely of azure (8) pixels.

2.  **Check for Existing Red Shape:** Determine if the are any shapes of red (2) cells.

3.  **Conditional Transformation:**
    *   **If a leftmost azure column exists AND an existing red shape exists:** Extend the red shape down and to the left, diagonally, by one red cell.
    *   **If no azure column is found:** Return the input grid unchanged.
"""

import numpy as np

def find_leftmost_azure_column(grid):
    """Finds the index of the leftmost column containing only '8' (azure)."""
    rows, cols = grid.shape
    for j in range(cols):
        is_azure_column = True
        for i in range(rows):
            if grid[i, j] != 8:
                is_azure_column = False
                break
        if is_azure_column:
            return j
    return -1


def find_red_shapes(grid):
    """Finds and returns a list of coordinates of red (2) pixels."""
    red_pixels = []
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:
                red_pixels.append((i, j))
    return red_pixels


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the leftmost azure column
    azure_column_index = find_leftmost_azure_column(output_grid)

    # Find red pixels
    red_pixels = find_red_shapes(output_grid)
    
    # Conditional transformations
    if azure_column_index != -1 and len(red_pixels) > 0:
        # extend each red pixel by one diagonally down and to the left
        for r, c in red_pixels:
            if r + 1 < rows and c -1 >= 0:
                output_grid[r + 1, c - 1] = 2
    elif azure_column_index == -1:
      # no change
        output_grid = np.copy(input_grid)

    return output_grid
```
