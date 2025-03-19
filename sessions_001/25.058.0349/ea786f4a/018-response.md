# ea786f4a • 018 • refine_coder

---
```python
"""
The transformation identifies the locations of white pixels (value 0) in the input grid.
For each white pixel, it draws a line of white pixels in the output grid. The shape and
extent of this line are determined by the row and column indices of the white pixel
in the input grid. Specifically, if a white pixel is found at (r, c) in the input, the
output grid will have a white line from (0, c) to (height-1, c) and from (r, 0) to
(r, width-1), where 'height' and 'width' are input_grid dimensions.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the coordinates of all white pixels (value 0)
    white_pixels_rows, white_pixels_cols = np.where(input_grid == 0)

    # Iterate through each white pixel found
    for row, col in zip(white_pixels_rows, white_pixels_cols):
        # Draw a vertical line: set all pixels in the column 'col' to white (0)
        output_grid[:, col] = 0
        # Draw a horizontal line: Set all pixels in row 'row' to white (0)
        output_grid[row, :] = 0

    return output_grid
```
