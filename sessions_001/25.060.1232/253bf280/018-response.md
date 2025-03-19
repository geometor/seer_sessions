# 253bf280 • 018 • refine_coder

---
```python
"""
Copy the input grid to the output grid. For each row, find all occurrences of azure pixels ('8'). If a row contains two or more '8's, replace all pixels between and including the first and last '8' with green pixels ('3'). Ensure the '8' pixels in the identified locations remain in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        # Find indices of all '8's in the current row
        indices_of_8 = np.where(input_grid[r] == 8)[0]

        # Check if there are at least two '8's in the row
        if len(indices_of_8) >= 2:
            # Get the first and last index of '8'
            start_index = indices_of_8[0]
            end_index = indices_of_8[-1]

            # Fill the space between the first and last '8' with '3's in the output grid
            output_grid[r, start_index:end_index+1] = 3
            
            # ensure that the 8's are still present
            for i in indices_of_8:
                output_grid[r,i] = 8

    return output_grid
```
