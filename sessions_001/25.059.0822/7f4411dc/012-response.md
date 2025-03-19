# 7f4411dc • 012 • refine_coder

---
```python
"""
1.  **Identify Magenta Pixels:** Locate all pixels with the color magenta (6) in the input grid.

2.  **Preserve Isolated Corner Pixel:** If a magenta pixel is located at the extreme top-right corner of the grid, preserve this magenta pixel.

3. **Preserve Edge Pixel** If a magenta pixel exists in the middle of the left edge of the grid (row = height/2, where height equals number of rows - 1, and column = 0) , preserve it

4. **Preserve larger contiguous blocks:** Identify contiguous blocks of magenta pixels (where pixels are directly adjacent horizontally or vertically). If a contiguous block contains more than two magenta pixels, preserve all pixels within that block.

5.  **Preserve Grid of 4:** If magenta pixels form a 2x2 grid anywhere on the canvas, they are preserved

6.  **All Other Pixels:** All other pixels in the output grid should be white (0).
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def flood_fill(grid, r, c, visited):
    """Performs a flood fill to identify a contiguous block of magenta pixels."""
    rows, cols = grid.shape
    if (r, c) in visited or grid[r, c] != 6:
        return []

    block = []
    stack = [(r, c)]
    visited.add((r,c))

    while stack:
        current_r, current_c = stack.pop()
        block.append((current_r, current_c))

        for neighbor_r, neighbor_c in get_neighbors(grid, current_r, current_c):
            if (neighbor_r, neighbor_c) not in visited and grid[neighbor_r, neighbor_c] == 6:
                stack.append((neighbor_r, neighbor_c))
                visited.add((neighbor_r, neighbor_c))
    return block

def check_2x2_grid(grid, r, c):
    """Checks if a 2x2 magenta grid exists starting at (r, c)."""
    rows, cols = grid.shape
    if r + 1 < rows and c + 1 < cols:
        if (grid[r, c] == 6 and grid[r + 1, c] == 6 and
            grid[r, c + 1] == 6 and grid[r + 1, c + 1] == 6):
            return True
    return False


def transform(input_grid):
    """
    Transforms the input grid based on the rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)  # Initialize with white (0)

    # Identify all magenta pixels
    magenta_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 6]
    visited = set()

    for r, c in magenta_pixels:
        # Preserve top-right corner pixel
        if r == 0 and c == cols - 1:
            output_grid[r, c] = 6
        # Preserve middle left edge pixel
        elif r == (rows -1) // 2 and c == 0:
            output_grid[r,c] = 6
        # Check and preserve 2x2 grids
        elif check_2x2_grid(input_grid, r, c):
            output_grid[r,c] = 6
            output_grid[r+1, c] = 6
            output_grid[r, c+1] = 6
            output_grid[r+1, c+1] = 6
            visited.add((r,c))
            visited.add((r+1,c))
            visited.add((r, c+1))
            visited.add((r+1, c+1))


    # contiguous blocks
    for r, c in magenta_pixels:
        if (r,c) not in visited:
            magenta_block = flood_fill(input_grid, r, c, visited)
            if len(magenta_block) > 2:
                for pixel_r, pixel_c in magenta_block:
                    output_grid[pixel_r, pixel_c] = 6

    return output_grid.tolist()
```
