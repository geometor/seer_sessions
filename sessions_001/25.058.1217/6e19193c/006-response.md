# 6e19193c • 006 • refine_coder

---
```python
"""
Transforms the input grid by mirroring orange pixels across the main diagonal only if other non-orange, non-black pixels exist.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of non-orange (7) and non-black (0) pixels.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy to preserve original pixels

    # Check for the presence of other colors
    other_colors_present = np.any((input_grid != 0) & (input_grid != 7))

    # Conditional Mirroring
    if other_colors_present:
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 7:
                    output_grid[c, r] = 7  # Mirror across the diagonal

    return output_grid.tolist()
```

