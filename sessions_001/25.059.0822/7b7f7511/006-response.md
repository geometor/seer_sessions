# 7b7f7511 • 006 • refine_coder

---
```python
"""
The transformation rule is to remove the last column of the input grid. The width is reduced by 1, but keep all rows.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Get the number of columns in the input grid
    num_cols = input_array.shape[1]
    
    # Create a list of column indices to keep (all except the last one)
    cols_to_keep = list(range(num_cols - 1))
    
    # Use array slicing to select the columns to keep
    output_array = input_array[:, cols_to_keep]
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
```
