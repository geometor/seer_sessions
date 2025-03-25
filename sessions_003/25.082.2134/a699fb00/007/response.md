```python
"""
For each row in the input grid, iterate through the cells. If a cell is '1' (blue),
check if there are any subsequent '1's in the same row. If there are, insert a '2'
(red) immediately after the first '1'. Maintain the original row length.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Initialize with a copy
    rows, cols = input_grid.shape

    for r in range(rows):
        insert_flag = False
        for c in range(cols):
            if input_grid[r, c] == 1:
                insert_flag = False
                for c2 in range(c + 1, cols):
                    if input_grid[r, c2] == 1:
                        insert_flag = True
                        break
                if insert_flag:
                    temp_row = list(output_grid[r])
                    temp_row.insert(c + 1, 2)
                    output_grid[r] = np.array(temp_row[:cols])


    return output_grid.tolist()
```
