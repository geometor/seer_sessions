# f35d900a • 019 • refine_coder

---
```python
"""
1.  **Identify colored pixels:** Find all red (value 2) and yellow (value 4) pixels in the input grid.
2.  **Vertical Expansion:** For each red and yellow pixel, if there are no other colored pixels (2 or 4) in the same *column*, expand the pixel vertically by adding copies of the pixel immediately above and below its original position. If the expansion would go beyond the grid boundary, stop at the edge.
3. **Gray Pixel Insertion:** Find vertically adjacent red and yellow expanded regions. Insert a single row of gray pixels (value 5) in empty rows immediately above and below the region where the red and yellow are adjacent.
"""

import numpy as np

def get_colored_pixels(grid, color):
    """Finds coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def expand_vertically(grid, coord):
    """Expands a pixel vertically if no other colored pixels are in the same column."""
    row, col = coord
    height, width = grid.shape
    output_grid = np.copy(grid)
    color = grid[row, col]

    # Check for other colored pixels in the same column
    has_colored_neighbor_col = any(grid[r, col] in [2, 4] and r != row for r in range(height))

    if not has_colored_neighbor_col:
        # Expand vertically
        if row > 0:
            output_grid[row - 1, col] = color
        if row < height - 1:
            output_grid[row + 1, col] = color
    return output_grid

def insert_gray_pixels(grid):
    """Inserts gray pixels between vertically adjacent red and yellow regions."""
    height, width = grid.shape
    output_grid = np.copy(grid)

    for r in range(height - 1):
        for c in range(width):
            # Check for vertically adjacent red and yellow pixels
            if (grid[r, c] == 2 and grid[r + 1, c] == 4) or (grid[r, c] == 4 and grid[r + 1, c] == 2):
                # Insert gray above if possible and empty
                if r > 0 and output_grid[r - 1, c] == 0:
                    output_grid[r - 1, c] = 5
                # Insert gray below if possible and empty
                if r + 2 < height and output_grid[r + 2, c] == 0:
                    output_grid[r + 2, c] = 5
    return output_grid
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Expand red and yellow pixels vertically
    red_pixels = get_colored_pixels(input_grid, 2)
    for coord in red_pixels:
        output_grid = expand_vertically(output_grid, coord)

    yellow_pixels = get_colored_pixels(input_grid, 4)
    for coord in yellow_pixels:
        output_grid = expand_vertically(output_grid, coord)
        
    # Insert gray pixels between adjacent regions
    output_grid = insert_gray_pixels(output_grid)

    return output_grid
```
