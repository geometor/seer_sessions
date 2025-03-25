```python
"""
The transformation rule is as follows:
1. Maintain '5' (gray pixels): Copy all instances of the digit '5' from the input grid to the same positions in the output grid.
2. Left Side Transformation: For each non-'5' digit in the input grid to the *left* of a '5', replace it based on a specific mapping.
3. Right Side Transformation: For each non-'5' digit to the *right* of a '5', transform them using a specific mapping.
4. If a zero is encountered to the left or to the right, but before a non-zero value, it transforms to 6.

Mapping:
    left:
        0: 6
        1: 6
        2: 7
        3: 8
        4: 9
    right:
        0: 6
        1: 6
        2: 7
        3: 8
        4: 9
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)   # Initialize output_grid
    rows, cols = input_grid.shape

    left_mapping = {0: 6, 1: 6, 2: 7, 3: 8, 4: 9}
    right_mapping = {0: 6, 1: 6, 2: 7, 3: 8, 4: 9}

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 5  # Keep 5s
            else:
                # Find nearest 5 to the left and right
                left_5 = -1
                for i in range(c - 1, -1, -1):
                    if input_grid[r, i] == 5:
                        left_5 = i
                        break

                right_5 = -1
                for i in range(c + 1, cols):
                    if input_grid[r, i] == 5:
                        right_5 = i
                        break

                if left_5 != -1 and c > left_5 : # and right_5 == -1:
                    output_grid[r, c] = left_mapping.get(input_grid[r, c], input_grid[r,c])

                elif right_5 != -1 and c < right_5:
                    output_grid[r, c] = right_mapping.get(input_grid[r, c], input_grid[r,c])
                elif input_grid[r,c] == 0:
                    output_grid[r,c] = 6
                

    return output_grid.tolist()
```