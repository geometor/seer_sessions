# 06df4c85 • 012 • refine_coder

---
```python
"""
Identify non-blue pixels adjacent to blue pixels horizontally.
Duplicate these pixels to the right based on their color:
- Red and yellow: Duplicate one position to the right.
- Azure and maroon: Duplicate three positions to the right.
- Green: Duplicate one position to the right.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is non-blue and adjacent to a blue pixel horizontally
            if input_grid[r, c] != 1:
                is_adjacent_to_blue = False
                if c > 0 and input_grid[r, c-1] == 1:  # Check left neighbor
                    is_adjacent_to_blue = True
                if c < cols - 1 and input_grid[r, c+1] == 1:  # Check right neighbor
                    is_adjacent_to_blue = True

                if is_adjacent_to_blue:
                    color = input_grid[r, c]
                    # Apply duplication rules based on color
                    if color in [2, 4, 3]:  # Red, yellow, green
                        if c + 1 < cols:
                            output_grid[r, c+1] = color
                    elif color in [8, 9]:  # Azure, maroon
                        for i in range(1, 4):
                            if c + i < cols:
                                output_grid[r, c+i] = color

    return output_grid
```
