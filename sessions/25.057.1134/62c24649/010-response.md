# 62c24649 • 010 • refine_coder

---
```python
"""
The output grid dimensions are double that of the input grid dimensions. The input grid is replicated to all four corners of the larger output grid. The edges between the corners are filled by replicating corresponding rows/columns from the input grid.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions (doubled)
    output_rows = input_rows * 2
    output_cols = input_cols * 2

    # Initialize output grid with zeros
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy the input grid to the center of the output grid
    output_grid[input_rows//2:input_rows//2 + input_rows, input_cols//2:input_cols//2 + input_cols] = input_grid
    
    # Replicate Corners:
    output_grid[0:input_rows//2, 0:input_cols//2] = input_grid[0:input_rows//2, 0:input_cols//2]  # Top-left
    output_grid[0:input_rows//2, output_cols-input_cols//2:] = input_grid[0:input_rows//2, input_cols-input_cols//2:]  # Top-right
    output_grid[output_rows-input_rows//2:, 0:input_cols//2] = input_grid[input_rows-input_rows//2:, 0:input_cols//2]  # Bottom-left
    output_grid[output_rows-input_rows//2:, output_cols-input_cols//2:] = input_grid[input_rows-input_rows//2:, input_cols-input_cols//2:]  # Bottom-right

    # Replicate Edges:
    # Top edge (excluding corners)
    output_grid[0:input_rows//2, input_cols//2:output_cols-input_cols//2] = input_grid[0:input_rows//2,:]
    # Bottom edge (excluding corners)
    output_grid[output_rows-input_rows//2:, input_cols//2:output_cols-input_cols//2] = input_grid[input_rows-input_rows//2:,:]
    # Left edge (excluding corners)
    output_grid[input_rows//2:output_rows-input_rows//2, 0:input_cols//2] = input_grid[:, 0:input_cols//2]
    # Right edge (excluding corners)
    output_grid[input_rows//2:output_rows-input_rows//2, output_cols-input_cols//2:] = input_grid[:, input_cols-input_cols//2:]

    return output_grid
```

