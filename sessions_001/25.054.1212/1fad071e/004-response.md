# 1fad071e • 004 • refine_coder

---
```python
"""
Divides the input grid into five vertical regions and checks for the presence of vertically contiguous blue (1) pixels in each region, starting from the top.
Outputs a 1x5 grid where each cell is blue (1) if the corresponding input region contained such blue pixels, and white (0) otherwise.
"""

import numpy as np

def _has_contiguous_blue(region):
    """
    Checks if a region has vertically contiguous blue pixels starting from the top.
    """
    rows, cols = region.shape
    if rows == 0 or cols == 0:  # Handle empty regions
        return False

    found_blue = False
    for c in range(cols):
        if region[0, c] == 1: # check the first row for blue
            found_blue = True
            for r in range(1,rows):
                if region[r,c] != 1:
                    break # contiguous block is broken
            # we found blue in the top row of this col, and checked for contiguous, so return
            return True
    
    return found_blue

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_height, input_width = input_grid.shape
    output_width = 5
    output_grid = np.zeros((1, output_width), dtype=int)  # Initialize output grid with white (0)

    # Calculate region width.  Handle cases where the width is not perfectly divisible.
    region_width = input_width // output_width
    extra_pixels = input_width % output_width
    
    start_col = 0
    for i in range(output_width):
        # Distribute any extra pixels across the regions, one at a time.
        current_region_width = region_width + (1 if i < extra_pixels else 0)
        end_col = start_col + current_region_width

        # Extract the current region
        region = input_grid[:, start_col:end_col]

        # Check for the presence of vertically contiguous blue (1) in the region
        if _has_contiguous_blue(region):
            output_grid[0, i] = 1  # Set output pixel to blue (1)

        start_col = end_col # move to the next region

    return output_grid
```
