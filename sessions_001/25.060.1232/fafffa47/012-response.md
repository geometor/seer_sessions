# fafffa47 • 012 • refine_coder

---
```python
"""
The input grid is reduced to the upper 3xN subgrid, where N is the original width.
Maroon (9) becomes red (2), all other colors are unchanged.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get dimensions of input
    height = input_array.shape[0]
    width = input_array.shape[1]

    # Initialize an empty 3xN output grid filled with white (0).
    output_grid = np.zeros((3, width), dtype=int)

    # Process the upper subgrid (first 3 rows).
    for i in range(min(3, height)):  # Ensure we don't go out of bounds
        for j in range(width):
            if input_array[i, j] == 9:  # If the cell is maroon (9)
                output_grid[i, j] = 2  # Change it to red (2)
            else:
                output_grid[i,j] = input_array[i,j]

    return output_grid.tolist()
```
