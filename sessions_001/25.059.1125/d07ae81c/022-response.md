# d07ae81c • 022 • refine_coder

---
```python
"""
1.  **Identify Central Stripe:** Locate the vertical column(s) of blue (1) pixels in the center of the grid. There can be one, two, or three adjacent center columns forming the stripe.
2.  **Central Stripe Transformation:** Change all blue (1) pixels within the identified central stripe to green (3).
3.  **Mirroring:** Mirror the grid content from left to right, using the central stripe as the axis of symmetry.
4.  **Conditional Color Change (Mirrored):** Within the mirrored regions, change blue (1) pixels to green (3).
5.  **Azure Preservation:**  Azure (8) pixels that are adjacent to the central stripe in the input, and are therefore also present in the mirrored locations, remain azure (8) in the output.
6.  **Green and Magenta Interaction:** If a green (3) pixel is at the edge (leftmost or rightmost in its row), and there isn't another green to the right of it, place a magenta (6) pixel immediately to its right, provided the space exists and will not overlap another.
7. All other pixels are unaffected by the transformation
"""

import numpy as np

def find_central_stripe(grid):
    """Finds the central vertical stripe(s) of blue (1) pixels."""
    height, width = grid.shape
    center_col = width // 2
    stripe_cols = []

    # Check for blue(1) in up to three center columns
    for col_offset in range(-1, 2):
        col = center_col + col_offset
        if 0 <= col < width and all(grid[:, col] == 1):
            stripe_cols.append(col)

    return stripe_cols

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = input_grid.copy()
    height, width = input_grid.shape
    stripe_cols = find_central_stripe(input_grid)

    # Central Stripe Transformation (Rule 2)
    for col in stripe_cols:
        output_grid[:, col] = np.where(output_grid[:, col] == 1, 3, output_grid[:, col])

    # Mirroring and Conditional Color Change (Rules 3 and 4)
    for r in range(height):
        for c in range(width):
            if c not in stripe_cols:
                mirrored_col = width - 1 - c
                if mirrored_col >=0 and mirrored_col < width:
                  # Conditional change and Azure Preservation (Rules 4 & 5)
                  if input_grid[r, mirrored_col] == 1:
                      output_grid[r, c] = 3
                  elif input_grid[r, mirrored_col] == 8 and (mirrored_col + 1 in stripe_cols or mirrored_col -1 in stripe_cols):
                      output_grid[r,c] = 8

    # Green and Magenta Interaction (Rule 6)
    for r in range(height):
        for c in range(width):
            if output_grid[r, c] == 3:
                if c == width -1 or (c+1 < width and output_grid[r,c+1] != 3): # Check for green at edge
                    if c + 1 < width:
                        output_grid[r, c + 1] = 6
    return output_grid
```
