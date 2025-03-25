```python
"""
Transforms an input grid by applying a specific color sequence pattern around each blue (1) pixel found in the input. The output grid maintains the same dimensions as the input. The color sequence is: 7 (one position left, up), 2( one position left), 1 (center), 6 (one position right), 8 (one position down and right).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy to preserve original grid
    rows, cols = input_grid.shape

    # Iterate through the input grid to find blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                # Apply the transformation rule for each blue pixel
                # 7 (one position up left)
                if r -1 >= 0 and c - 1 >= 0 :
                    output_grid[r - 1, c - 1] = 7
                # 2 one left
                if  c - 1 >= 0 :
                    output_grid[r, c - 1] = 2
                # 1 (center - already copied, doing again for clarity)
                output_grid[r,c] = 1
                # 6 (one position right)
                if c + 1 < cols:
                    output_grid[r, c + 1] = 6
                # 8 (one position down, right)
                if r + 1 < rows and c + 1 < cols:
                    output_grid[r + 1, c + 1] = 8

    return output_grid
```
