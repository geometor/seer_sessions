# b782dc8a • 004 • example_1 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid.
Check if the current pixel is NOT azure (8).
If not azure (8) examine the four neighbor pixels (up, down, left, right)
Iterate over the four neighbors.
If any neighbor is azure (8) then:
  - Change the neighboring azure (8) pixel to green(3) if the last non-azure pixel was not green
  - Change the neighboring azure(8) pixel to red(2) if the last non-azure pixel was not red
  - Reset the 'last non-azure pixel' at each non-azure pixel, start with the last non azure was red.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    last_non_azure = 2  # Initialize with red

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 8:  # Check if NOT azure
                last_non_azure = 2 # reset to red for each new non-azure start
                # Check neighbors
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))  # Up
                if r < rows - 1: neighbors.append((r + 1, c))  # Down
                if c > 0: neighbors.append((r, c - 1))  # Left
                if c < cols - 1: neighbors.append((r, c + 1))  # Right

                for nr, nc in neighbors:
                    if output_grid[nr, nc] == 8:  # If neighbor is azure
                        if last_non_azure != 3:
                            output_grid[nr, nc] = 3  # Change to green
                            last_non_azure = 3
                        elif last_non_azure !=2:
                            output_grid[nr, nc] = 2  # Change to red
                            last_non_azure = 2


    return output_grid
```
