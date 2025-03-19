# 963e52fc • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to horizontally stretch a colored band (alternating blue (1) and red (2) pixels) by duplicating each of its columns while leaving the white (0) background untouched.
"""

import numpy as np

def find_colored_band(grid):
    # Find the rows containing alternating blue (1) and red (2) pixels.
    rows, cols = grid.shape
    band_rows = []
    for r in range(rows):
        row = grid[r]
        is_band_row = False
        if row[0] == 1 or row[0] == 2: # Check start of band
          is_band_row = True
          for i in range(cols - 1):
            if row[i] == row[i + 1] or (row[i]!= 1 and row[i]!=2):
              is_band_row = False
              break
        if is_band_row:
            band_rows.append(r)
    return band_rows

def transform(input_grid):
    # Initialize output_grid with expanded width
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)


    # Find the rows that make up the colored band
    band_rows = find_colored_band(input_grid)

    # Copy the background and stretch the colored band
    for r in range(rows):
        if r not in band_rows:
            # Copy background rows directly, doubling the width
            for c in range(cols):
              output_grid[r, c*2] = input_grid[r,c]
              output_grid[r, c*2 + 1] = input_grid[r,c]

        else:
            # Stretch the colored band rows
            for c in range(cols):
                output_grid[r, 2 * c] = input_grid[r, c]
                output_grid[r, 2 * c + 1] = input_grid[r, c]

    return output_grid
```
