# d631b094 • 016 • example_3 • investigate_coder

---
```python
"""
Examine the input grid.
Identify the single non-zero pixel within the grid.
Create a 1x1 output grid containing only the value of that identified non-zero pixel.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Find the indices of non-zero elements.
    non_zero_indices = np.nonzero(input_array)
    
    # Check if there's exactly one non-zero element.
    if len(non_zero_indices[0]) == 1:
        # Extract the non-zero value.
        non_zero_value = input_array[non_zero_indices[0][0], non_zero_indices[1][0]]
        
        # Create a 1x1 output grid with the non-zero value.
        output_grid = [[non_zero_value]]
        
        return output_grid
    else:
       # if there are no, or more than one non zero pixels return an empty grid,
       # for now, we'll handle only the case we were shown
       return [[]]
```
