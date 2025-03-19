# 6455b5f5 • 012 • refine_coder

---
```python
"""
Finds a vertical line of red pixels in the input grid. The background white pixels to the right of the vertical red line are changed to azure, and the rest of the white pixels are changed to blue.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find all pixels of the specified color
    color_pixels = np.argwhere(grid == color)

    # Find the vertical arm: Find range for rows
    if len(color_pixels) > 0:
        min_row = np.min(color_pixels[:, 0])
        max_row = np.max(color_pixels[:, 0])
    
        # Find the column that defines the vertical arm by checking for contiguous pixels
        vertical_arm_col = -1
        for col in np.unique(color_pixels[:, 1]):
            contiguous_pixels = []
            for row in range(min_row, max_row + 1):
                if grid[row, col] == color:
                  contiguous_pixels.append( (row, col) )

            if len(contiguous_pixels) == (max_row - min_row + 1):
                vertical_arm_col = col
                break
        return vertical_arm_col

    return -1

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the column index of the vertical arm of the red pixels
    vertical_arm_col = find_vertical_line(input_grid, 2)
    
    if (vertical_arm_col >= 0):
        # Iterate through the grid and change colors based on the position relative to the vertical arm
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 0:  # If it's white
                    if c > vertical_arm_col:
                        output_grid[r, c] = 8  # Change to azure
                    else:
                        output_grid[r, c] = 1  # Change to blue
    return output_grid
```
