# b2862040 • 026 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies contiguous regions of blue (1) pixels within a maroon (9) grid.
If a blue region has more than one pixel, it changes the color of those pixels to azure (8).
Isolated blue pixels and the maroon background remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors (up, down, left, right) of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def get_contiguous_region(grid, start_row, start_col, color):
    """Finds a contiguous region of a given color starting from a given cell."""
    region = set()
    queue = [(start_row, start_col)]
    visited = set()

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited:
            continue
        visited.add((row, col))

        if grid[row, col] == color:
            region.add((row, col))
            neighbors = get_neighbors(grid, row, col)
            queue.extend(neighbors)
    return region

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    # Iterate through all cells in the grid
    for row in range(rows):
        for col in range(cols):
            # If we find a blue pixel that hasn't been visited yet
            if input_grid[row, col] == 1 and (row, col) not in visited:
                # Get the contiguous region of blue pixels it belongs to
                region = get_contiguous_region(input_grid, row, col, 1)
                visited.update(region)

                # If the region has more than one pixel
                if len(region) > 1:
                    # Change all pixels in the region to azure (8)
                    for r, c in region:
                        output_grid[r, c] = 8

    return output_grid
```
