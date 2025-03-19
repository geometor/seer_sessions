# ce602527 • 018 • refine_coder

---
```python
"""
Extracts a 3x3 block centered on a specific target pixel (azure, blue, or magenta).
"""

import numpy as np

def find_target_pixel(grid):
    # Find azure (8), blue (1) or magenta(6) pixels
    target_colors = [8, 1, 6]
    for color in target_colors:
        target_pixels = np.argwhere(grid == color)
        if len(target_pixels) > 0:
            # Return the first target pixel found
            return target_pixels[0]
    return None

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # Find the target pixel (azure, blue, or magenta)
    target_pixel = find_target_pixel(input_grid)

    # If no target pixel is found, return an empty grid
    if target_pixel is None:
        return []

    # Calculate the coordinates of the 3x3 block
    row, col = target_pixel
    min_row = row - 1
    max_row = row + 1
    min_col = col - 1
    max_col = col + 1

    # Handle edge cases
    min_row = max(0, min_row)
    max_row = min(input_grid.shape[0] - 1, max_row)
    min_col = max(0, min_col)
    max_col = min(input_grid.shape[1] - 1, max_col)
    
    # Extract the block
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```
