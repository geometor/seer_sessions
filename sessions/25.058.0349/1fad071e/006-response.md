# 1fad071e • 006 • refine_coder

---
```python
"""
1. Count Blue Pixels: Count the number of blue pixels (1) in the input grid. This count will be the first value in the output.
2. Determine Row Count: Count the number of rows in the input grid. This will be the second number in the output.
3. Determine Column Count: In example 4, the third number in the output is the column count. Add this.
4. Pad with Zeroes: The output grid is always 1x5. Pad the remaining values of the output with zeros.
"""

import numpy as np

def transform(input_grid):
    # Count blue pixels
    blue_count = 0
    for row in input_grid:
        for pixel in row:
            if pixel == 1:  # Blue is represented by 1
                blue_count += 1

    # Get the number of rows
    num_rows = len(input_grid)
    
    # Get the number of cols
    num_cols = len(input_grid[0]) if num_rows > 0 else 0

    # Create the output grid (1x5) and populate it
    output_grid = np.array([[blue_count, num_rows, num_cols, 0, 0]])

    return output_grid.tolist()
```
