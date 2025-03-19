# 00d62c1b • 032 • refine_coder

---
```python
"""
1.  **Background Check:** If the input grid contains no white pixels, no transformation is performed. The output is identical to the input.
2.  **Green Pixel Preservation:** If a green pixel has at least one white neighbor (up, down, left, or right), it remains green.
3. **Green to Yellow Tranformation**: If a green pixel is completely surrounded by other green pixels (up, down, left, and right), it changes to yellow.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def has_white_neighbor(grid, row, col):
    """Checks if a cell has any white neighbors."""
    neighbors = get_neighbors(grid, row, col)
    return any(neighbor == 0 for neighbor in neighbors)

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Background Check: If no white pixels, return input grid.
    if 0 not in input_grid:
        return output_grid

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Green Pixel Preservation and Transformation
            if input_grid[row, col] == 3:  # If pixel is green
                if has_white_neighbor(input_grid, row, col):
                    output_grid[row, col] = 3 # Remain green
                elif all(neighbor == 3 for neighbor in get_neighbors(input_grid, row, col)):
                    output_grid[row, col] = 4  # Change to yellow
    return output_grid
```
