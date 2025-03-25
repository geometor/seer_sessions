```python
"""
The transformation rule takes an input grid with a single blue (1) pixel in the bottom-left corner and generates an output grid with an alternating pattern of blue (1) and azure (8) pixels. The output grid has the same height as the input and twice the width. The alternating pattern starts from the bottom-left, ensuring the original blue pixel's location is part of the new pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Generate alternating pattern
    for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0: # even sum -> azure (8)
                if row % 2 == 1: # odd row
                    output_grid[row, col] = 1
                else:
                    output_grid[row,col] = 8
            else: # odd sum  -> blue (1)
                if row % 2 == 1: # odd row
                   output_grid[row, col] = 8
                else:
                    output_grid[row,col] = 1


    return output_grid
```