```python
"""
The transformation identifies contiguous regions of azure (8) pixels in the input grid. 
It then replaces the "border" azure pixels of each region with red (2) pixels and the remaining interior azure pixels with blue (1) pixels. 
Background (0) pixels remain unchanged.  Border pixels are defined by 8-connectivity.
Isolated azure pixels are also turned red.
"""

import numpy as np

def get_all_neighbors(grid, row, col):
    """Gets all 8 neighbors (including diagonals) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            if (r, c) != (row, col):  # Exclude the cell itself
                neighbors.append((r, c))
    return neighbors

def is_border_or_isolated(grid, row, col, color):
    """Checks if a cell of the specified color is a border cell or isolated."""
    if grid[row, col] != color:
        return False

    neighbors = get_all_neighbors(grid, row, col)
    all_same_color = all(grid[r, c] == color for r, c in neighbors)
    return not all_same_color
    

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find azure regions and apply replacements
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8:  # Found an azure pixel
                if is_border_or_isolated(input_grid, row, col, 8):
                    output_grid[row, col] = 2  # Replace border/isolated azure with red
                else:
                    output_grid[row, col] = 1  # Replace interior azure with blue

    return output_grid
```