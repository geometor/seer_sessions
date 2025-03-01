# 6430c8c4 • 018 • refine_coder

---
```python
"""
1. Divide and Conquer: Divide the input grid into non-overlapping 2x2 pixel regions.
2. Output Dimension: The output grid's dimensions are determined by dividing the input grid's dimensions by two, rounding down for both height and width.
3. Process Regions: For each 2x2 region in the input grid:
    *   If *any* pixel within the region is *not* white (0), the corresponding pixel in the output grid is set to green (3).
    *   If *all* pixels within the region are white (0), the corresponding pixel in the output grid is set to white (0).
4. Output Generation: The output is the resulting grid created in step 3.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows // 2
    output_cols = cols // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through 2x2 regions
    for i in range(output_rows):
        for j in range(output_cols):
            # Extract the 2x2 region from the input grid
            region = input_grid[i*2:(i+1)*2, j*2:(j+1)*2]
            
            # Check if any non-white pixel exists in the region
            if np.any(region != 0):
                output_grid[i, j] = 3  # Set output pixel to green
            else:
                output_grid[i, j] = 0  # Set output pixel to white

    return output_grid.tolist()
```

