```python
"""
1.  **Identify White Pixels:** Locate all pixels in the input grid with a value of 0 (white).

2.  **Replace and Recolour:** For each identified white pixel:

    *   Replace the white (0) pixel itself with a new color, the selection rules are:
        *   In train_1 example 1, the replacement is:
            *   red (2) if original white pixel is at an even row and even column index
            *   green (3) if original white pixel is at an odd row and odd column index
            *    blue(1) if white pixel is at odd row and even column or even row and odd column
        *    In train_2 example 2, the replacement is:
            *   red (2) if original white pixel is at an even row and even column index
            *   green (3) if original white pixel is at an odd row and odd column index
            *    blue(1) if white pixel is at odd row and even column or even row and odd column
        *   In train_3 example 3, the replacement is:
            *   red (2) if original white pixel is at an even row and even column index
            *   green (3) if original white pixel is at an odd row and odd column index
            *    blue(1) if white pixel is at odd row and even column or even row and odd column

    *   Change the colors of some neighboring gray(5) pixels.
        * If the pixel to the immediate left of the original white is gray(5), change it, the selection rules are:
            * In train_1, change to red(2)
            * In train_2, change to red(2)
            * In train_3, change to red(2)
       * If the pixel to the immediate right of the original white is gray(5), change it, the selection rules are:
            * In train_1, change to red(2)
            * In train_2, change to red(2)
            * In train_3, change to red(2)
       * If the pixel to the immediate top of the original white is gray(5), change it, the selection rules are:
            * In train_1, change to blue(1)
            * In train_2, change to blue(1)
            * In train_3, change to blue(1)
      * If the pixel to the immediate bottom of the original white is gray(5), change it, the selection rules are:
            * In train_1, change to green(3)
            * In train_2, change to green(3)
            * In train_3, change to green(3)
3.  **Preserve Other Pixels:** All other pixels (those not white and not immediately adjacent to white pixels in the input) remain unchanged in value.

4. **Output:** construct the final output grid.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                # Determine replacement color for the white pixel
                if (i % 2 == 0 and j % 2 == 0):
                    output_grid[i, j] = 2  # Red
                elif (i % 2 != 0 and j % 2 != 0):
                    output_grid[i, j] = 3  # Green
                else:
                    output_grid[i, j] = 1  # Blue

                # Change neighboring gray pixels
                if j > 0 and input_grid[i, j - 1] == 5:  # Left
                    output_grid[i, j - 1] = 2  #red
                if j < cols - 1 and input_grid[i, j + 1] == 5:  # Right
                    output_grid[i, j + 1] = 2 #red
                if i > 0 and input_grid[i - 1, j] == 5:  # Top
                    output_grid[i - 1, j] = 1 #blue
                if i < rows - 1 and input_grid[i + 1, j] == 5:  # Bottom
                    output_grid[i + 1, j] = 3 #green

    return output_grid
```
