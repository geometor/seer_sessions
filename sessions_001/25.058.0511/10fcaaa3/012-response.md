# 10fcaaa3 • 012 • refine_coder

---
```python
"""
1.  **Double Dimensions:** The output grid's dimensions (height and width) are double that of the input grid.
2.  **2x2 Block Replication:** For each pixel in the input grid, create a 2x2 block of cells in the output grid.
3.  **Color Mapping:** The color of the input pixel is copied to *all four* cells of the corresponding 2x2 block in the output grid.
4.  **Position Mapping** The top-left corner of each 2x2 block will be at position output[2*row, 2*col] relative to the input pixel at input[row, col].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for row in range(input_height):
      for col in range(input_width):
        #replicate input pixels in 2x2 block
        output_grid[row*2, col*2] = input_grid[row,col]
        output_grid[row*2+1, col*2] = input_grid[row,col]
        output_grid[row*2, col*2+1] = input_grid[row,col]
        output_grid[row*2+1, col*2+1] = input_grid[row,col]
        

    return output_grid
```

