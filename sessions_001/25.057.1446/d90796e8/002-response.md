# d90796e8 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify**: Locate the non-zero numbers in the top row of the input grid.
2. **Sum**: Calculate sum of those numbers.
3.  **Replace**: Replace the first non-zero number in the top row (scanning left-to-right) with the result calculated in the previous step.
4. **Clear**: Set all other numbers in top row to 0.
5. **Preserve**: Keep every number not in the top row as in the original input
6.  **Output**: The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify non-zero numbers in the top row
    top_row_numbers = []
    for j in range(cols):
        if output_grid[0, j] != 0:
            top_row_numbers.append((0, j, output_grid[0, j]))

    # Sum the identified numbers, handling empty list case
    if top_row_numbers:
      sum_of_numbers = sum([num for _, _, num in top_row_numbers])
    
      first_non_zero_index = top_row_numbers[0][1]

      # replace
      output_grid[0,first_non_zero_index] = (top_row_numbers[0][2] + top_row_numbers[1][2]) if len(top_row_numbers) > 1 else top_row_numbers[0][2] * 2

    # clear the other pixels
    for j in range(cols):
      if output_grid[0,j] != 0:
        if j != first_non_zero_index:
           output_grid[0,j] = 0
    

    return output_grid
```
