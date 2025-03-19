# a85d4709 • 016 • refine_coder

---
```python
"""
Replaces gray pixels with red. The center white pixel becomes yellow.  White pixels that form a contiguous 3x3 block *with* the center pixel remain white. Other white pixels become red.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Gray (5) pixels become Red (2).
    - White (0) pixels become Yellow (4) if in the center.
    - White pixels stay white if they are part of a contiguous 3x3 block centered on the center pixel.
    - Other white pixels become Red (2).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace gray (5) with red (2)
    output_grid[output_grid == 5] = 2

    # Check for center pixel and replace white (0) with yellow (4)
    if rows % 2 != 0 and cols % 2 != 0: #check for odd sized grid
        center_row, center_col = rows // 2, cols // 2
        if output_grid[center_row, center_col] == 0:
            output_grid[center_row, center_col] = 4

        # Define the 3x3 block around the center
        block_start_row = max(0, center_row - 1)
        block_end_row = min(rows, center_row + 2)
        block_start_col = max(0, center_col - 1)
        block_end_col = min(cols, center_col + 2)

        # Iterate through all white pixels
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 0:
                    # Check if the white pixel is within the 3x3 block
                    if block_start_row <= r < block_end_row and block_start_col <= c < block_end_col:
                        #Keep as White (0)
                        pass
                    else:
                        # Change other whites to red.
                        output_grid[r,c] = 2

    else:
        # Replace remaining white (0) with red (2) - for even sized grids
        output_grid[output_grid == 0] = 2
    
    return output_grid
```
