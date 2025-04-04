# 3-1e0a9b12 • 006 • example_3 - CODE

---
```python
"""
The transformation rule operates on each column of the grid independently. For each column, the goal is to rearrange the numbers such that all non-zero numbers are moved to the bottom of the column, while the top positions are filled with zeros. The relative vertical order of the non-zero numbers within each column is maintained.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving non-zero numbers in each column to the bottom.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
    
    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each column
    for j in range(cols):
        # Extract non-zero numbers from the current column
        non_zero_elements = input_grid[:, j][input_grid[:, j] != 0]
        
        # Count the number of non-zero elements
        num_non_zero = len(non_zero_elements)
        
        # Fill the bottom 'num_non_zero' rows of the output column with the extracted numbers
        output_grid[rows - num_non_zero:, j] = non_zero_elements
        
        # Fill the remaining top rows with zeros (this is already done during initialization)

    return output_grid.tolist()
```

