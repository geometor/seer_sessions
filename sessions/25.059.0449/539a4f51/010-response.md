# 539a4f51 • 010 • refine_coder

---
```python
"""
1.  **Determine Background Color:** Find the most frequent color in the *input* grid. This is the background color.
2.  **Initialize Output Grid:** Create an output grid that is twice the width and twice the height of the input grid. Fill the output grid with the background color.
3.  **Expand Non-Background Pixels:** Iterate through each pixel of the input grid.
    *   If a pixel is *not* the background color, expand it into a 2x2 block of the same color in the output grid.
    *   The top-left corner of the 2x2 block in the output grid corresponds to the row and column of the input pixel multiplied by 2 (output_row = input_row * 2, output_col = input_col * 2).
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Finds the most frequent color in a grid."""
    # Flatten the grid to a 1D list and use Counter to count pixel values
    color_counts = Counter(grid.flatten().tolist())
    # Return most frequent
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = input_height * 2
    output_width = input_width * 2

    # Determine background color from the *input grid*
    background_color = get_background_color(np.array(input_grid))


    # initialize output_grid with the background color
    output_grid = np.full((output_height, output_width), background_color)

    # Iterate through input grid
    for row_index in range(input_height):
        for col_index in range(input_width):
            input_pixel_value = input_grid[row_index][col_index]
            #if a non-background cell
            if input_pixel_value != background_color:
              # set the corresponding 2x2 block in output.
              output_grid[row_index*2:row_index*2+2, col_index*2:col_index*2+2] = input_pixel_value

    return output_grid
```
