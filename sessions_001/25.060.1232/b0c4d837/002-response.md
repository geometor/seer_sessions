# b0c4d837 • 002 • example_6 • investigate_coder

---
```python
"""
The transformation extracts the azure rectangle from within a grey "U" shape in the input grid. 
It then creates a 3x3 output grid. The first row of the output grid represents the azure rectangle, 
with a maximum of three azure pixels. If the input rectangle has more than three azure pixels horizontally, 
the output alternates azure and white pixels in the first row, starting with azure.
"""

import numpy as np

def find_rectangle(grid, color):
    # Find coordinates of pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, max_row, min_col, max_col
    

def transform(input_grid):
    # Find the azure rectangle.
    min_row, max_row, min_col, max_col = find_rectangle(input_grid, 8)
    
    # Initialize the output grid as 3x3 with all white pixels.
    output_grid = np.zeros((3, 3), dtype=int)

    if min_row is not None:
       # Determine the azure pixel representation in the output.
        width = max_col - min_col + 1
        
        output_col = 0
        for col in range(min_col, max_col + 1):
           if output_col < 3:
              if width <= 3 or (col - min_col) % 2 == 0 :
                  output_grid[0, output_col] = 8
              else:
                output_grid[0, output_col] = 0
              output_col += 1
              
    return output_grid
```
