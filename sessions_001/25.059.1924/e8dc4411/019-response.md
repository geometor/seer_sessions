# e8dc4411 • 019 • refine_coder

---
```python
"""
1.  **Identify Azure Pixels:** Locate all pixels with a value of 8 (azure) in the input grid.
2.  **Conditional Expansion:** For each azure pixel:
    *   Check if it's within the top two rows
    * Check if all these conditions are true:
        *   The pixel to the immediate right is empty (value 0).
        *   The pixel below *that* empty cell is yellow (value 4).
    *  If so, the empty cell to the right of the original azure pixel becomes an azure pixel (8).
3. **Yellow Preservation**: Yellow Pixels are unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the top two rows
    for r in range(min(2, rows)):  # Ensure we don't go out of bounds
        for c in range(cols):
            # Find azure pixels
            if input_grid[r, c] == 8:
                # Check conditions for expansion
                if c + 1 < cols and input_grid[r, c + 1] == 0 and r + 1 < rows and input_grid[r + 1, c + 1] == 4:
                    output_grid[r, c + 1] = 8  # Expand azure to the right

    return output_grid
```

