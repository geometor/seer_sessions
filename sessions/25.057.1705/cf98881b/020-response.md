# cf98881b • 020 • example_4 • investigate_coder

---
```python
"""
The transformation extracts specific columns from the input grid, picks selected elements, and rearranges them into a smaller 4x4 output grid. The transformation primarily focuses on the yellow (4), maroon (9), and blue (1) pixels and their relative positions in the input grid's 4th, 9th and 13th columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 4x4 array filled with yellow (4).
    output_grid = np.full((4, 4), 4, dtype=int)

    # Extract relevant pixels from the input grid
    # From 4th column: all yellow (4) - already in output
    # From 9th column: elements at 2nd and 3rd row which are maroon (9)
    # From 13th column: element at the 4th row which is blue(1)
    
    if input_grid.shape[1] >= 9: #making sure we do not go out of bound
       output_grid[1, 1] = input_grid[1, 8]  # 2nd row, 9th column (index 8)
       output_grid[2, 1] = input_grid[2, 8]  # 3rd row, 9th column (index 8)

    if input_grid.shape[1] >=13:
        output_grid[3, 0] = input_grid[3, 12]  # 4th row, 13th column (index 12)

    output_grid[0,0] = 0
    
    return output_grid
```
