```python
"""
The transformation rule is as follows:

1.  **Identify Pivot:** Locate all occurrences of the digit '5' (gray) within the input grid. These '5's remain unchanged in the output grid.

2.  **Left Transformation:** For any digit *to the left* of a '5', apply the following transformation:
    *   0 becomes 6
    *   1 becomes 6
    *   2 becomes 7
    *   3 becomes 8
    *   4 becomes 9

3.  **Right Transformation:** For any digit *to the right* of a '5', apply the following transformation:
    *   0 becomes 6
    *   1 becomes 6
    *   2 becomes 7
    *   3 becomes 8
    *   4 becomes 9

4.  **Output:** Create the output grid with the transformed digits based on their position relative to any '5's, copying the '5' digits as they appear.
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

                if left_5 != -1 and c > left_5:
                    output_grid[r, c] = left_mapping.get(input_grid[r, c], input_grid[r,c])
                elif right_5 != -1 and c < right_5:
                    output_grid[r, c] = right_mapping.get(input_grid[r, c], input_grid[r,c])


    return output_grid.tolist()
```