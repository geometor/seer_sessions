# b8cdaf2b • 017 • refine_coder

---
```python
"""
Transforms rows of all white pixels in the input grid to rows with blue pixels at the ends and white pixels in the middle.
Other rows are copied unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each row of the input grid
    for i, row in enumerate(input_grid):
        # Check if all pixels in the row are white (0)
        if np.all(row == 0):
            # Create a new row for the output grid
            new_row = np.zeros_like(row)
            # Set the first and last pixels to blue (1)
            new_row[0] = 1
            new_row[-1] = 1
            # keep other pixels white (0) - already initialized
            # Replace the corresponding row in the output_grid with new_row
            output_grid[i] = new_row

    return output_grid
```
