# c3f564a4 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to identify and remove '0' (white) pixels within a repeating "1 2 3 4 5" sequence in a grid, and replace them with the correct number of the sequence, maintaining the pattern horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing '0' pixels with the appropriate
    value from the repeating sequence "1 2 3 4 5".
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:
                # Determine the expected value based on the horizontal sequence
                expected_horizontal = (j % 5) + 1

                # Determine the expected value based on the vertical sequence
                expected_vertical = (i % 5) + 1
                
                # prioritize horizontal, check if correct
                if i > 0 and output_grid[i-1][j] == expected_horizontal:
                    output_grid[i][j] = expected_horizontal
                elif i < rows - 1 and (output_grid[i+1][j] == expected_horizontal - 1 or (expected_horizontal-1 == 0 and output_grid[i+1][j] == 5 )):
                      output_grid[i][j] = expected_horizontal
                # otherwise, replace with the verticle
                else:
                    output_grid[i][j] = expected_vertical



    return output_grid
```
