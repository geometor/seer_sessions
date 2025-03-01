# 662c240a • 008 • example_1 • investigate_coder

---
```python
"""
Extracts the bottom-right 3x3 subgrid from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 subgrid.
    
    Args:
        input_grid (list of lists): The input grid.
    
    Returns:
        list of lists: The bottom-right 3x3 subgrid.
    """
    # Convert the input grid to a NumPy array for easier slicing.
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    rows, cols = input_array.shape
    
    # Extract the bottom-right 3x3 subgrid using array slicing.
    output_array = input_array[rows-3:rows, cols-3:cols]
    
    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid
```

