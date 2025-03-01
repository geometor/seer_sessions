# d07ae81c • 020 • refine_coder

---
```python
"""
The transformation identifies a central blue stripe in the input grid and mirrors/shifts parts of it in the output grid. Blue (1) pixels become green (3) based on their position relative to the center and other colors. Green (3) pixels are preserved, and a single magenta (6) pixel appears to the right.  Azure (8) pixels appear to follow different, complex rules based on mirroring.
"""

import numpy as np

def find_central_stripe(grid):
    """Finds the central vertical stripe of blue (1) pixels."""
    height, width = grid.shape
    center_col = width // 2
    stripe_cols = []

    # Check for blue(1) in up to three center columns
    for col_offset in range(-1,2):
        col = center_col + col_offset
        if 0 <= col < width and all(grid[:, col] == 1):
            stripe_cols.append(col)

    return stripe_cols


def transform(input_grid):
    """Transforms the input grid."""
    output_grid = input_grid.copy()
    height, width = input_grid.shape
    stripe_cols = find_central_stripe(input_grid)

    # Iterate through the grid
    for r in range(height):
        for c in range(width):

            # Mirroring and recoloring based on central stripe
            dist_to_center = abs(c - width // 2)

            if dist_to_center > 0 and dist_to_center <= len(stripe_cols):
                mirrored_col = width - 1 - c  # Correct mirroring

                if mirrored_col < width and mirrored_col >= 0:
                  if input_grid[r,mirrored_col] == 8:
                      output_grid[r, c] = 8 # Azure
                  if input_grid[r,mirrored_col] == 1 and input_grid[r,c] ==1:
                      output_grid[r, c] = 3

            # Central stripe recoloring
            if c in stripe_cols:
                if input_grid[r, c] == 1:
                    output_grid[r, c] = 3 # all blue becomes green

            # Preserve and highlight green (only one to the right)
            if input_grid[r, c] == 3:
                magenta_placed = False
                if c + 1 < width and input_grid[r,c+1] != 3:
                    output_grid[r,c+1] = 6 #Magenta
                    magenta_placed = True

                if magenta_placed == True and c + 2 < width and input_grid[r,c+2] == 6:
                    output_grid[r,c+2] = input_grid[r,c+2]

    return output_grid
```
