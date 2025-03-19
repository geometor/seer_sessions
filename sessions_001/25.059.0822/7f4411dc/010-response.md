# 7f4411dc • 010 • example_2 • investigate_coder

---
```python
"""
The transformation identifies contiguous blocks of magenta (6) pixels in the input grid. It then filters these blocks based on a size/connectivity criterion, removing isolated or small blocks while preserving larger ones. The output grid has the same dimensions as the input, with only the qualifying magenta blocks remaining, and all other pixels set to white (0).
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
    

def transform(input_grid):
    """
    Transforms the input grid by removing isolated or small magenta blocks, keeping larger connected ones.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)  # Initialize output grid with all white (0)
    visited = set()
    
    # Iterate through the grid to find magenta blocks
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 6 and (r,c) not in visited:
                magenta_block = flood_fill(input_grid, r, c, visited)

                # Apply the filtering rule: Keep blocks with more than 2 pixels
                if len(magenta_block) > 2:
                    for pixel_r, pixel_c in magenta_block:
                        output_grid[pixel_r, pixel_c] = 6  # Set magenta pixel in output

    return output_grid
```
