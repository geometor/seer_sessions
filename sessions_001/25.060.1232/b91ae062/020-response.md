# b91ae062 • 020 • refine_coder

---
```python
"""
The input grid's pixels are expanded into 3x3 blocks in the output grid. The output grid's dimensions are three times the input's dimensions. Each pixel in the input becomes a 3x3 block of the same color in the output.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Calculate output grid dimensions
    output_rows = input_rows * 3
    output_cols = input_cols * 3

    # Initialize output_grid as an empty array with calculated dimensions
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each cell of the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the value of the current cell
            value = input_grid[i][j]

            # Expand the cell into a 3x3 block in the output grid
            for row in range(3 * i, 3 * (i + 1)):
                for col in range(3 * j, 3 * (j + 1)):
                    output_grid[row][col] = value

    return output_grid.tolist()
```

