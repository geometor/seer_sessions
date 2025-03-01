# 74dd1130 • 008 • refine_coder

---
```python
"""
The transformation rule examines the input grid. If the input grid has any rows that are composed of only black (0) pixels, remove them from the top of the image until the top row has a non-black pixel. If there are no rows that are all black, then return the original image with no changes.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_np_grid = np.array(input_grid)

    # Find the index of the first row that contains a non-zero element
    non_zero_rows = np.any(input_np_grid != 0, axis=1)
    first_non_zero_row_index = np.argmax(non_zero_rows)

    # if there are no non-zero rows, then return original
    if first_non_zero_row_index == 0 and np.any(input_np_grid[0] != 0):
        output_grid = input_grid
    # Crop the array to remove all-zero rows from the top
    else:
       output_grid = input_np_grid[first_non_zero_row_index:].tolist()

    return output_grid
```
