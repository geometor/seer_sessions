# 6ecd11f4 • 012 • refine_coder

---
```python
"""
Locate all 3x3 subgrids within the input grid. For each subgrid, copy only the non-white pixels (value not 0) to a new 3x3 output grid, preserving their relative positions. If multiple 3x3 subgrids exist, process each independently.
"""

import numpy as np

def find_all_subgrids(grid, size=3):
    """Finds all 3x3 subgrids within a given grid."""
    subgrids = []
    rows, cols = grid.shape
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            subgrid = grid[i:i+size, j:j+size]
            subgrids.append(((i, j), subgrid))  # Store top-left coordinates and the subgrid
    return subgrids

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find all 3x3 subgrids
    subgrids = find_all_subgrids(input_grid)

    # Initialize the output grid (3x3) - will be overwritten for each subgrid
    output_grid = np.zeros((3, 3), dtype=int)

    # Process each subgrid
    for (start_row, start_col), subgrid in subgrids:
        # Create a temporary 3x3 grid for each subgrid
        temp_grid = np.zeros((3, 3), dtype=int)

        # Copy non-white pixels, maintaining relative position
        for i in range(3):
            for j in range(3):
                if subgrid[i, j] != 0:
                    temp_grid[i, j] = subgrid[i, j]
        output_grid = temp_grid # keep the last one
    
    return output_grid.tolist()
```

