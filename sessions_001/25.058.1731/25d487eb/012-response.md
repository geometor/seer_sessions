# 25d487eb • 012 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to identify an "arrowhead" shape made of azure (8) pixels with a green (3) pixel at its base. Then a vertical line of green (3) pixels is added, starting from the top row of the grid and extending downwards for 5 pixels, aligned with the column of the green base pixel of the arrowhead.
"""

import numpy as np

def find_arrowhead_base(grid):
    # Find the green pixel (3)
    rows, cols = np.where(grid == 3)
    if len(rows) > 0:
        return rows[0], cols[0]  # Assuming only one green pixel
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the base of the arrowhead (green pixel)
    base_coords = find_arrowhead_base(input_grid)

    if base_coords:
        _, base_col = base_coords

        # Draw the vertical green line
        for row in range(5):
            output_grid[row, base_col] = 3

    return output_grid
```
