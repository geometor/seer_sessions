# 6cdd2623 • 010 • example_2 • investigate_coder

---
```python
"""
1. **Identify Red Rows:** Iterate through each row of the input grid. For each row, check if it contains at least one red (2) pixel.
2. **Fill Identified Rows:** For each row identified in step 1, change the color of *all* pixels in that row to red (2).
3. **Clear Remaining Pixels:** For all other rows (those that *do not* contain any red pixels in the input), set all pixels in the output grid to white (0).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by filling rows containing red pixels with red and clearing others."""

    output_grid = np.zeros_like(input_grid)  # Initialize output_grid with zeros (white)

    # Iterate through rows
    for i, row in enumerate(input_grid):
        # Check if the row contains any red (2) pixels
        if 2 in row:
            # Fill the entire row with red (2) in the output grid
            output_grid[i, :] = 2
        else:
            # set all other pixels to white, which they are
            # already initialized to
            pass
    
    return output_grid
```

