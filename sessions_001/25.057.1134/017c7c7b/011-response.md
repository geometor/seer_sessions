# 017c7c7b • 011 • refine_coder

---
```python
"""
1.  **Color Substitution:** Examine every pixel in the input grid. If a pixel is blue (color value 1), change it to red (color value 2) in the output grid.
2.  **Conditional Row Extension:**
    *   Inspect input for adjacent rows and columns that exhibit an alternating, "checkerboard" pattern of blue and azure pixels.
    *   Inspect input to ensure all blue cells are adjacent to one another.
    *   If *both* conditions above are true, extend output grid by appending three rows to the bottom.
    *   The extended rows are copies of existing rows.
    *   If conditions are not met, output has the same shape as input.
"""

import numpy as np

def check_checkerboard(grid):
    # Check for checkerboard pattern of blue (1) and azure (8)
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 1:
                if not ((grid[r+1, c] == 8 and grid[r, c+1] == 8) or
                        (grid[r+1,c] == 0 and grid[r,c+1] == 0)):  # also check for black
                    return False
            elif grid[r, c] == 8:
                if not ((grid[r+1, c] == 1 and grid[r, c+1] == 1) or
                       (grid[r+1, c] == 0 and grid[r, c+1] == 0)):   # also check for black
                    return False
            elif grid[r,c] == 0:
                if not ((grid[r+1,c] == 1 or grid[r+1,c] == 8) and
                        (grid[r,c+1] == 1 or grid[r,c+1] == 8)):
                    return False
    return True

def check_blue_adjacency(grid):
    # Check if all blue (1) pixels are adjacent
    rows, cols = grid.shape
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                blue_pixels.append((r, c))

    if not blue_pixels:
        return True  # No blue pixels, vacuously true

    # Check adjacency using a simple BFS
    visited = set()
    queue = [blue_pixels[0]]
    visited.add(blue_pixels[0])

    while queue:
        r, c = queue.pop(0)
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in blue_pixels and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(visited) == len(blue_pixels)

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Replace all blue (1) pixels with red (2)
    output_grid[output_grid == 1] = 2

    # Check if row extension is needed
    if check_checkerboard(input_grid) and check_blue_adjacency(input_grid):
        # Get dimensions of original grid
        rows, cols = output_grid.shape

        # Create the extension rows as numpy array.  The existing output_grid establishes
        # the checkerboard pattern, so just duplicate a slice.
        extension = np.copy(output_grid[0:3,:])

        # Vertically stack to add to bottom
        output_grid = np.vstack((output_grid, extension))

    return output_grid
```
