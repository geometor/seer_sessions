```python
"""
The input grid is transformed into a larger output grid by scaling each pixel to a 2x2 block. The scaled blocks are then arranged in the output grid by reflecting the input both horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into the output grid by scaling each pixel to a 2x2 block and arranging
    these blocks based on horizontal and vertical reflections.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Iterate through each cell of the input grid
    for i in range(input_height):
        for j in range(input_width):
            # Scale each pixel to a 2x2 block
            value = input_grid[i][j]

            # Top-left quadrant: Original
            output_grid[2*i][2*j] = value
            output_grid[2*i+1][2*j] = value
            output_grid[2*i][2*j+1] = value
            output_grid[2*i+1][2*j+1] = value

            # Top-right quadrant: Horizontal reflection
            output_grid[2*i][output_width - 2*j - 1] = value
            output_grid[2*i+1][output_width - 2*j - 1] = value
            output_grid[2*i][output_width - 2*j - 2] = value
            output_grid[2*i+1][output_width - 2*j - 2] = value

            # Bottom-left quadrant:  Vertical reflection
            output_grid[output_height - 2*i - 1][2*j] = value
            output_grid[output_height - 2*i - 2][2*j] = value
            output_grid[output_height - 2*i - 1][2*j+1] = value
            output_grid[output_height - 2*i - 2][2*j+1] = value

            # Bottom-right quadrant: Horizontal and Vertical reflection
            output_grid[output_height - 2*i - 1][output_width - 2*j - 1] = value
            output_grid[output_height - 2*i - 2][output_width - 2*j - 1] = value
            output_grid[output_height - 2*i - 1][output_width - 2*j - 2] = value
            output_grid[output_height - 2*i - 2][output_width - 2*j - 2] = value

    return output_grid
```
