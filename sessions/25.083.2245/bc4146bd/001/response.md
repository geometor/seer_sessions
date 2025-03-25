```python
"""
The input grid's pattern is replicated and tiled to form an output grid that is 5 times larger in both dimensions. Each cell in the input grid corresponds to a 5x5 block of the same value in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Create Output Grid
    output_height = input_height * 5
    output_width = input_width * 5
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Tile input grid
    for row in range(input_height):
        for col in range(input_width):
            value = input_grid[row][col]
            # Fill a 5x5 block in the output grid with the current value
            output_grid[row*5:row*5+5, col*5:col*5+5] = value

    return output_grid
```