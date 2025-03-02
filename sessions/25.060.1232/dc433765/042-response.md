# dc433765 • 042 • refine_coder

---
```python
"""
Combine all green objects into a single pixel at the center of the grid. Keep yellow and blue pixels at their original positions. Set all other pixels to black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as all black (0)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the center coordinates
    center_row, center_col = rows // 2, cols // 2

    # Flag to check if green pixel is placed at center.
    green_placed = False

    # Iterate through the input grid
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 3:  # Green pixel
                # Place only one green pixel in the center
                if not green_placed:
                    output_grid[center_row, center_col] = 3
                    green_placed = True
            elif input_grid[i, j] == 4 or input_grid[i,j] == 1:  # Yellow or Blue pixel
                # Keep yellow and blue pixels at their original positions
                output_grid[i, j] = input_grid[i, j]
            # Implicitly, other pixels remain 0 (black) as initialized

    return output_grid
```
