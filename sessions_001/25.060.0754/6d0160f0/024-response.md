# 6d0160f0 • 024 • refine_coder

---
```python
"""
The transformation preserves horizontally contiguous sequences of gray (5) pixels and converts all other pixels to white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with white (0).
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid.
    for r in range(rows):
        # Iterate through each column, keeping track of contiguous gray sequences.
        current_run = []
        for c in range(cols):
            if input_grid[r, c] == 5:
                current_run.append(c)
            else:
                # If the current pixel is not gray, check if we had a run.
                if current_run:
                    # If there was a run, copy the gray pixels to the output.
                    for col_index in current_run:
                        output_grid[r, col_index] = 5
                    current_run = []  # Reset the run.
        # Handle the case where a run extends to the end of a row.
        if current_run:
            for col_index in current_run:
                output_grid[r, col_index] = 5

    return output_grid
```
