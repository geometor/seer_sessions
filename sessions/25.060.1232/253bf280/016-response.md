# 253bf280 • 016 • example_3 • investigate_coder

---
```python
"""
Identify rows with multiple '8's. Fill the space between the first and last '8' in those rows with '3's in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of input_grid
    rows, cols = input_grid.shape     # Get grid dimensions
    
    for r in range(rows):            # Iterate through rows
        indices_of_8 = np.where(input_grid[r] == 8)[0]  # find indices of 8s in the row
        if len(indices_of_8) >= 2:  # Check for at least two 8s
            start_index = indices_of_8[0]         # first 8
            end_index = indices_of_8[-1]          # last 8
            output_grid[r, start_index:end_index+1] = 3  # fill 3s
            for i in indices_of_8:                   # ensure 8's are copied
                output_grid[r,i] = 8
            
    return output_grid
```
