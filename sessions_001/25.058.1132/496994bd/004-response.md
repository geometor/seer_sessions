# 496994bd • 004 • example_1 • investigate_coder

---
```python
"""
1. Copy the top three rows of the input grid.
2. Reverse the order of copied rows.
3. Paste the reversed rows into the bottom three rows of the output grid.
4. Copy the middle four rows (rows 4-7) of input grid to output grid, keeping them in same positions.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Copy the top three rows
    top_three_rows = np.copy(input_grid[:3])

    # Reverse the order of the copied rows
    reversed_rows = top_three_rows[::-1]

    # Paste the reversed rows into the bottom three rows of the output grid
    output_grid[-3:] = reversed_rows
    
    # rows 4-7 are unchanged, handled during initialization

    return output_grid
```

