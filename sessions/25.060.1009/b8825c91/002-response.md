# b8825c91 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Enclosed Regions:** Examine the input grid. Identify all "enclosed regions." An enclosed region is defined as a contiguous group of pixels of the same color, completely surrounded by a different, single color. Contiguous means 4-way connectivity (up, down, left, right - not diagonal). The surrounding "border" pixels must all be of the same color.

2.  **Replace Interior Color:** For each enclosed region, replace the color of the enclosed region's pixels with the color of the surrounding border pixels. If the border has more than 1 unique color the region is not changed.

3. **Other pixels**: all other pixels keep original value.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 4-connected neighbors of a pixel."""
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

def is_enclosed(grid, row, col, visited):
    """Checks if a region is enclosed and returns the border color and region."""
    rows, cols = grid.shape
    start_color = grid[row, col]
    stack = [(row, col)]
    region = []
    border_colors = set()
    visited.add((row, col))

    while stack:
        r, c = stack.pop()
        region.append((r, c))

        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
                if grid[nr, nc] == start_color:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
                else:
                    border_colors.add(grid[nr, nc])
            elif grid[nr,nc] != start_color:
                border_colors.add(grid[nr,nc])


    if len(border_colors) == 1:
        return border_colors.pop(), region
    else:
        return None, None

def transform(input_grid):
    """Transforms the input grid by filling enclosed regions."""
    
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    # Iterate through each pixel in the grid.
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                border_color, region = is_enclosed(input_grid, row, col, visited)
                if border_color is not None:
                    for r, c in region:
                        output_grid[r, c] = border_color # fill

    return output_grid
```
