# 810b9b61 • 008 • refine_coder

---
```python
"""
1.  **Identify Enclosed Regions:** Identify all contiguous regions of pixels, regardless of their color, that are completely enclosed by blue (1) pixels. "Completely enclosed" means there's no path from any pixel within the region to the edge of the grid without crossing a blue pixel.

2.  **Transform Boundary Pixels:** Change the color of all blue (1) pixels that form the boundary of these enclosed regions to green (3).

3.  **Preserve Other Pixels:** All pixels that are not part of the identified blue boundaries retain their original color.
"""

import numpy as np
from collections import deque

def is_enclosed(grid, start_row, start_col):
    """
    Checks if a region is enclosed by blue pixels using a flood fill algorithm.
    Handles any color for the enclosed region.
    """
    rows, cols = grid.shape
    start_color = grid[start_row, start_col]  # Get the color of the starting pixel
    if start_color == 1: # starting on blue is not useful
        return False

    visited = set()
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Check if we've reached the edge of the grid
        if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
            return False  # Not enclosed

        # Explore adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] == start_color and (nr, nc) not in visited:
                    queue.append((nr, nc))
                # If we encounter blue, we stop exploring in that direction (it's a boundary)

    return True  # Enclosed

def find_enclosing_blue_pixels(grid):
    """
    Finds all blue pixels that are part of an enclosing region.
    Considers regions of any color enclosed by blue.
    """
    rows, cols = grid.shape
    enclosing_blue_pixels = set()

    # Find all regions and check if they are enclosed
    regions = []
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and (r, c) not in visited:  # Start flood fill for non-blue pixels
                if is_enclosed(grid, r, c):
                    regions.append((r, c))
                # mark this region as visited so we don't process again.
                queue = deque([(r, c)])
                start_color = grid[r,c]
                while queue:
                    row, col = queue.popleft()
                    if (row, col) in visited:
                        continue
                    visited.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == start_color and (nr, nc) not in visited:
                            queue.append((nr, nc))

    # For each enclosed region, find the surrounding blue pixels
    for start_row, start_col in regions:
        queue = deque([(start_row, start_col)])
        visited_region = set()
        while queue:
            row, col = queue.popleft()
            if (row, col) in visited_region:
                continue
            visited_region.add((row,col))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr, nc] == 1:
                        enclosing_blue_pixels.add((nr, nc))
                    elif (nr, nc) not in visited_region and grid[nr,nc] == grid[start_row, start_col]:
                        queue.append((nr, nc))

    return enclosing_blue_pixels
    

def transform(input_grid):
    """
    Transforms the input grid by changing blue pixels enclosing regions of any color to green.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixels that enclose white regions
    enclosing_blue_pixels = find_enclosing_blue_pixels(input_grid)

    # change output pixels
    for row, col in enclosing_blue_pixels:
        output_grid[row, col] = 3

    return output_grid
```
