# 9f236235 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms a large grid containing colored rectangular blocks into a smaller 4x4 grid,
representing the presence and relative positions of the colored blocks. The
transformation identifies red (2), blue (1), and green (3) blocks, selects a
single pixel from each, and places them in the output grid, maintaining their
top-to-bottom order. Azure (8) and most white (0) pixels are discarded.
"""

import numpy as np

def find_colored_blocks(grid):
    """Finds distinct colored blocks (2, 1, 3) in the grid."""
    blocks = {}
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, block):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, block)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color in [2, 1, 3] and (r, c) not in visited:
                block = []
                dfs(r, c, color, block)
                blocks[color] = block
    return blocks

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Initialize output_grid as a 4x4 array filled with 0 (white)
    output_grid = np.zeros((4, 4), dtype=int)

    # Find colored blocks (2, 1, 3)
    colored_blocks = find_colored_blocks(input_grid)

    # Sort the blocks by their top-most row appearance
    sorted_colors = sorted(colored_blocks.keys(), key=lambda color: min(r for r, _ in colored_blocks[color]))

    # Place one representative pixel from each block into the output grid
    row = 0
    for color in sorted_colors:
        output_grid[row, 0 if color!=2 else 2] = color  # place color and offset the red block to upper right.
        row += 1

    return output_grid
```
