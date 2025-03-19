# 3af2c5a8 • 016 • example_3 • investigate_coder

---
```python
"""
Expands the input grid by adding a green (3) border around it. The height is increased by 2, and the width is increased by 4. The original content is centered within the new grid.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate dimensions of the output grid
    output_height = input_height + 2
    output_width = input_width + 4

    # Initialize the output grid with green (3)
    output_grid = np.full((output_height, output_width), 3)

    # Copy the input grid into the center of the output grid
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i + 1][j + 2] = input_grid[i][j]

    return output_grid
```
