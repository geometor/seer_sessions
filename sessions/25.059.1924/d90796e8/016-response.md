# d90796e8 • 016 • example_3 • investigate_coder

---
```python
"""
Find adjacent red and green pixels, replace it with azure, while keeping all other colors unchanged.
"""

import numpy as np

def find_adjacent_red_green(grid):
    """Finds and returns the coordinates of adjacent red and green pixels."""
    red_green_pairs = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:  # Red pixel
                # Check right neighbor
                if c + 1 < cols and grid[r, c + 1] == 3:
                    red_green_pairs.append(((r, c), (r, c + 1)))
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
