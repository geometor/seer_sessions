# 272f95fa • 018 • refine_coder

---
```python
"""
1.  **Identify the Azure Cross:** Locate the cross-shaped structure formed by connected azure (8) pixels. The cross is defined by the longest horizontal and longest vertical lines of azure pixels. The intersection of these lines defines the center of the cross (central row and central column).

2.  **Retain Central Row:** Preserve the horizontal line of azure pixels that forms part of the cross.

3.  **Fill Above (Red):** Starting from the row immediately above the central row and at the central column, fill the connected region with red (2) upwards, stopping only when encountering an azure (8) pixel or the edge of the grid.

4.  **Fill Left Below (Magenta):** Starting from the row immediately below the central row and the column immediately to the left of the central column, fill the connected region with magenta (6) downwards and leftwards, stopping only when encountering an azure (8) pixel or the edge of the grid.

5.  **Fill Yellow Row:** On the row immediately below the central row, fill pixels with yellow (4) starting from one column left of the central column, moving left. Stop when encountering an azure pixel (8) or the edge of the grid.

6.  **Fill Right Below (Green):** Starting from the row immediately below the central row and the column immediately to the right of the central column, fill the connected region with green (3) downwards and rightwards, stopping only when encountering an azure (8) pixel or the edge of the grid.

7.  **Fill Bottom (Blue):** Fill the entire bottom row of the grid with blue (1), except for any positions where azure (8) pixels are already present.
"""

import numpy as np

def find_azure_cross(grid):
    """Finds the center coordinates of the azure cross, defined by longest lines."""
    rows, cols = grid.shape
    azure_pixels = np.where(grid == 8)
    
    # Find longest horizontal line
    row_counts = np.bincount(azure_pixels[0])
    central_row_index = np.argmax(row_counts)

    # Find longest vertical line
    col_counts = np.bincount(azure_pixels[1])
    central_col_index = np.argmax(col_counts)
    
    return central_row_index, central_col_index

def flood_fill(grid, start_row, start_col, fill_color, boundary_color):
    """Fills a region bounded by a specific color."""
    rows, cols = grid.shape
    if grid[start_row, start_col] == boundary_color or grid[start_row, start_col] == fill_color:
        return

    stack = [(start_row, start_col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and grid[r, c] != boundary_color and grid[r,c] != fill_color:
            grid[r, c] = fill_color
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the azure cross
    central_row_index, central_col_index = find_azure_cross(output_grid)

    # Fill Above (Red)
    flood_fill(output_grid, central_row_index - 1, central_col_index, 2, 8)

    # Fill Left Below (Magenta)
    flood_fill(output_grid, central_row_index + 1, central_col_index - 1, 6, 8)

    # Fill Yellow Row
    if central_row_index + 1 < rows:
        for c in range(central_col_index -1, -1, -1):
             if output_grid[central_row_index+1, c] == 8:
                break
             output_grid[central_row_index + 1, c] = 4
    
    # Fill Right Below (Green)
    flood_fill(output_grid, central_row_index + 1, central_col_index + 1, 3, 8)

    # Fill Bottom (Blue) - only on the last row
    if central_row_index+1<rows:
        for c in range(cols):
            if output_grid[rows-1,c] != 8:
                output_grid[rows - 1, c] = 1

    return output_grid
```

