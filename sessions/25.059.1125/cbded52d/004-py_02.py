"""
The transformation rule is as follows:
1.  **Initialization:** The input is an 8x8 grid of colored pixels.
2.  **Identify target:** check for pixels in the 5th column that are yellow or red.
3. **Identify Changing Pixels**: Locate blue pixels to the left of the target, and change the blue pixels to the color of the pixel on the 5th column.
4.  **Preservation:** All other pixels retain their original color and position.
5. **Output Production:** The output is the modified 8x8 grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of input_grid
    rows = len(input_grid)
    cols = len(input_grid[0])
   
    # Iterate through 5th column (index 4)
    for i in range(rows):
            if output_grid[i,4] == 4 or output_grid[i,4] == 2:
                target_color = output_grid[i,4]
                if output_grid[i,3] == 1:
                    output_grid[i,3] = target_color
    return output_grid