# d90796e8 • 018 • refine_coder

---
```python
"""
Identify and replace adjacent red and green pixels with azure, regardless of their order or direction of adjacency.
"""

import numpy as np

def find_adjacent_red_green(grid):
    """Finds and returns the coordinates of adjacent red and green pixels."""
    red_green_pairs = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:  # Red pixel
                # Check all eight neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the pixel itself
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 3:
                            red_green_pairs.append(((r, c), (nr, nc)))
            elif grid[r, c] == 3:  # Green pixel
                # Check all eight neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the pixel itself
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 2:
                            red_green_pairs.append(((r, c), (nr, nc)))
    return red_green_pairs

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find adjacent red and green pairs
    red_green_pairs = find_adjacent_red_green(output_grid)

    # Replace the found pairs with azure (8)
    for pair in red_green_pairs:
        output_grid[pair[0]] = 8
        output_grid[pair[1]] = 8
        

    return output_grid
```
