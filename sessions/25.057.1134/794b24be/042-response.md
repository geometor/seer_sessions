# 794b24be • 042 • refine_coder

---
```python
"""
1. Check for Blue: Examine the entire input grid. If any pixel is blue (1), proceed to step 2. Otherwise, the output is identical with the input.
2. Transform First Row: If blue is present, change all pixels in the *first* row of the output grid to red (2).
3. Keep remaining rows unchanged: The remaining rows in the output grid are the same as the input grid if blue is not present, and all 0 if the first row has been modified..
"""

import numpy as np

def has_blue(grid):
    """Checks if the grid contains any blue pixel (value 1)."""
    return np.any(grid == 1)

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Check if blue is present in input.
    if has_blue(input_grid):
        # If present, make first row of output_grid to red.
      output_grid[0, :] = 2
      # set the rest of the output grid to 0
      if output_grid.shape[0] > 1:
        output_grid[1:, :] = 0

    return output_grid
```
