# 8403a5d5 • 007 • refine_coder

---
```python
"""
1.  **Identify the Seed:** Find the first non-zero pixel in the input grid. This pixel is the "seed." Note its color and position (row, column).

2.  **Vertical Propagation:** Fill the entire column containing the seed with the seed's color.

3. **Insert 5**: Place a single 5 two rows above the seed, if possible.
"""

import numpy as np

def find_seed(grid):
    """Finds the first non-zero pixel's coordinates."""
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Find seed location
    seed_location = find_seed(input_grid)
    if seed_location is None:
        return output_grid

    seed_row, seed_col = seed_location
    seed_color = input_grid[seed_row, seed_col]

    # Vertical Propagation: Fill the seed's column with the seed's color.
    output_grid[:, seed_col] = seed_color

    # Insert 5: Two rows above the seed, in the same column.
    insert_row = seed_row - 2
    if insert_row >= 0:
        output_grid[insert_row, seed_col] = 5

    return output_grid
```
