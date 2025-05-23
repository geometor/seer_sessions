# 662c240a • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to crop the input grid to a 3x3 area at the bottom right.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the 3x3 subgrid from the lower-right corner of the input grid.
    """
    # Convert input_grid to a NumPy array for easier slicing
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input array
    rows, cols = input_array.shape
    
    # Calculate the starting indices for the 3x3 subgrid
    start_row = rows - 3
    start_col = cols - 3
    
    # Extract the 3x3 subgrid using array slicing
    output_array = input_array[start_row:rows, start_col:cols]
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
```

