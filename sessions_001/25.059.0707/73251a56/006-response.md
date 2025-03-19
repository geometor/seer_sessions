# 73251a56 • 006 • refine_coder

---
```python
"""
Replace all white pixels with the background color, magenta. Leave all other colored pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Define the background color (magenta).
    background_color = 6
    
    # Define the target color to replace (white).
    target_color = 0

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is white.
            if input_grid[row, col] == target_color:
                # Replace the white pixel with the background color (magenta).
                output_grid[row, col] = background_color

    return output_grid
```

