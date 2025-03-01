# 5582e5ca • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Examine the input grid.
2. Identify value that appears in both the upper-left and middle.
3. Create a new 3x3 grid.
4. Fill: All cells will contain this identified value.
5. Output the new grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify the value of the upper left cell
    target_value = input_grid[0][0]
    
    if input_grid[0][0] == input_grid[1][1]:
        target_value = input_grid[0][0]
    elif input_grid[0][1] == input_grid[1][1]:
        target_value = input_grid[0][1]
    elif input_grid[1][0] == input_grid[1][1]:
        target_value = input_grid[1][0]    

    # change output pixels 
    for i in range(3):
        for j in range(3):
            output_grid[i][j] = target_value

    return output_grid
```
