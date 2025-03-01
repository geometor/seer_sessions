# 681b3aeb • 018 • refine_coder

---
```python
"""
Finds all square subgrids within the input grid that consist of a single,
uniform color.  Copies the most top-left subgrid to a new output grid of the
same dimensions.
"""

import numpy as np

def find_uniform_square_subgrids(grid):
    """
    Finds all square subgrids within the input grid that have a uniform color.
    Returns a list of tuples: (row_start, col_start, size, color).
    """
    subgrids = []
    height, width = grid.shape
    for size in range(1, min(height, width) + 1):
        for row in range(height - size + 1):
            for col in range(width - size + 1):
                subgrid = grid[row:row+size, col:col+size]
                first_color = subgrid[0, 0]
                if np.all(subgrid == first_color):
                    subgrids.append((row, col, size, first_color))
    return subgrids

def transform(input_grid):
    input_grid = np.array(input_grid)
    subgrids = find_uniform_square_subgrids(input_grid)

    if not subgrids:
        # Handle cases where no uniform subgrids are found.
        # Returning an empty grid of a default size.
        return np.zeros((1,1), dtype=int)

    # Sort by row (top-most), then column (left-most)
    subgrids.sort(key=lambda x: (x[0], x[1]))
    top_left_subgrid = subgrids[0]
    row_start, col_start, size, _ = top_left_subgrid

    # Create output grid of the correct size
    output_grid = np.zeros((size, size), dtype=int)

    # Copy the selected subgrid to the output
    for i in range(size):
        for j in range(size):
            output_grid[i, j] = input_grid[row_start + i, col_start + j]

    return output_grid
```
