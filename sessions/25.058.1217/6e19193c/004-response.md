# 6e19193c • 004 • example_1 • investigate_coder

---
```python
"""
Mirrors the orange (7) pixels in the input grid across the main diagonal (top-left to bottom-right) and combines them with the original pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring orange pixels across the main diagonal.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
                # Keep original orange pixel
                output_grid[r, c] = 7
                # Mirror across the diagonal
                output_grid[c, r] = 7

    return output_grid.tolist() # convert back to list
```

