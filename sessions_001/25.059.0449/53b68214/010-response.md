# 53b68214 • 010 • example_2 • investigate_coder

---
```python
"""
The input grid is expanded vertically to double its height. The pattern of rows in the input grid, 
including a vertical green line at the third column (index 2), is repeated in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Determine the output grid dimensions (double the height)
    output_height = input_height * 2
    output_width = input_width

    # Initialize the output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Repeat the input grid pattern vertically
    for i in range(output_height):
        output_grid[i, :] = input_grid[i % input_height, :]

    return output_grid
```
