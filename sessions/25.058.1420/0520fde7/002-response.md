# 0520fde7 • 002 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid with a gray stripe to a 3x3 output grid.
Red pixels in the output correspond to the relative position of blue pixels
to the gray stripe in the input.
"""

import numpy as np

def find_gray_stripe_column(grid):
    # Find the column index of the vertical gray stripe (all cells are 5).
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen, based on problem definition


def transform(input_grid):
    # Initialize the 3x3 output grid with all zeros (white).
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the column index of the gray stripe.
    gray_stripe_col = find_gray_stripe_column(input_grid)

    # Iterate through the input grid to find blue pixels (value 1).
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 1:
                # Calculate the horizontal distance from the blue pixel to the gray stripe.
                distance = j - gray_stripe_col

                # Map the blue pixel to a red pixel in the output grid.
                output_row = i
                if output_row >= 3: # ensure the row is on the output grid
                    output_row = 2
                if distance < 0:  # Blue pixel is to the left.
                    output_grid[output_row, 0] = 2
                elif distance > 0:  # Blue pixel is to the right.
                    output_grid[output_row, 2] = 2
                else:  # Blue pixel is in the gray stripe.
                    output_grid[output_row, 1] = 2

    return output_grid
```
