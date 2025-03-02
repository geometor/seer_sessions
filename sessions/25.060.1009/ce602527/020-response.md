# ce602527 • 020 • refine_coder

---
```python
"""
Extracts a block centered on a specific target pixel (azure, blue, or magenta).
Handles edge cases by adjusting block size and returns an empty list if no target pixel is found.
"""

import numpy as np

def find_target_pixel(grid):
    """Finds the first occurrence of a target pixel (azure, blue, or magenta)."""
    target_colors = [8, 1, 6]
    for color in target_colors:
        target_pixels = np.argwhere(grid == color)
        if target_pixels.shape[0] > 0:
            return target_pixels[0]  # Return the first target pixel found
    return None

def transform(input_grid):
    """
    Transforms the input grid by extracting a block around a target pixel.
    """
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # Find the target pixel (azure, blue, or magenta)
    target_pixel = find_target_pixel(input_grid)

    # If no target pixel is found, return an empty list
    if target_pixel is None:
        return []

    # Calculate the coordinates of the block
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

