# a68b268e • 038 • refine_coder

---
```python
"""
1.  **Check for Separator:** Examine the input grid for a horizontal line composed entirely of blue (1) pixels.

2.  **Conditional Logic:**
    *   **If a blue separator exists:**
        1.  Consider all rows *below* the blue separator line as the "source region".
        2.  Create an output grid of size 4x4.
        3.  Fill the output with the color of the source region (excluding the single different colored pixel).
        4. copy the last row of the source region, and replace the last row of the 4x4 with that row

    *   **If no blue separator exists:**
        1. take the last row of the input
        2. create an output grid using that row
"""

import numpy as np

def find_blue_separator(input_grid):
    """Finds the row index of a horizontal blue (1) separator line, if it exists."""
    for i, row in enumerate(input_grid):
        if np.all(row == 1):
            return i
    return -1  # Return -1 if no separator is found

def get_source_region(input_grid, separator_index):
    """Extracts the region below the separator."""
    return input_grid[separator_index + 1:, :]

def get_majority_color(region):
    """ finds the dominant color ignoring the single diff colored pixel"""
    unique, counts = np.unique(region, return_counts=True)

    # find index of the max, unless it contains only 1 element.
    if counts.shape[0] > 1:
      max_index = np.argmax(counts[:-1])
    else:
      max_index = np.argmax(counts)

    return unique[max_index]

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find blue separator
    separator_index = find_blue_separator(input_grid)

    if separator_index != -1:
        # Separator exists
        source_region = get_source_region(input_grid, separator_index)
        majority_color = get_majority_color(source_region)
        output_grid = np.full((4, 4), majority_color, dtype=int)
        output_grid[3, :] = source_region[-1,:] # replace last row.
    else:
        # No separator
        output_grid = input_grid[-1:].copy() # last row

    return output_grid
```
