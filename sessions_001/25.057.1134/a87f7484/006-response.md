# a87f7484 • 006 • refine_coder

---
```python
"""
Find the azure pixel. The top-left corner of the output 3x3 region is one row
down and one column to the right of the azure pixel.
"""

import numpy as np

def find_azure_pixels(grid):
    """Finds coordinates of all azure pixels (color 8) in the grid."""
    return np.argwhere(grid == 8)

def get_target_region(grid, azure_coord):
    """
    Calculates the top-left corner and extracts the 3x3 region, handling
    out-of-bounds cases.
    """
    row, col = azure_coord
    target_row = row + 1
    target_col = col + 1

    # Check for out-of-bounds
    if (target_row + 2 >= grid.shape[0] or
        target_col + 2 >= grid.shape[1]):
        return None  # Indicate region is out of bounds

    return grid[target_row:target_row+3, target_col:target_col+3]


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all azure pixels
    azure_pixels = find_azure_pixels(input_grid)

    # Initialize output grid as empty
    output_grid = np.array([])

    # Process the first azure pixel found (if any)
    if azure_pixels.size > 0:
        # Extract the 3x3 region based on the first azure pixel
        region = get_target_region(input_grid, azure_pixels[0])
        if region is not None: # handle out of bound errors
          output_grid = region


    return output_grid.tolist()
```

