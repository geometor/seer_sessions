# 06df4c85 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to horizontally duplicate the red and green 2x2 blocks, while leaving the blue 2x2 blocks and the background unchanged.
"""

import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of the same color and returns their top-left coordinates and color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            color = grid[r, c]
            if (grid[r:r+2, c:c+2] == color).all():
                blocks.append((r, c, color))
    return blocks

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    blocks = find_2x2_blocks(output_grid)

    for r, c, color in blocks:
        # Conditional Replication
        if color == 2 or color == 3:  # Red or Green
            # Replicate horizontally to the right
            if c + 2 < cols: # Boundary check
                output_grid[r:r+2, c+2:c+4] = color
        # Blue blocks (color == 1) are left unchanged.
        # Background remains unchanged.

    return output_grid
```
