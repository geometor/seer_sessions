# d23f8c26 • 008 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid by extracting non-white pixels from the central column,
preserving their row index and color, and placing them in the central column of the output grid.
The rest of the output grid is filled with white pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input, filled with white (0).
    output_grid = np.zeros_like(input_grid)
    
    # Get the number of columns in the input grid.
    num_cols = input_grid.shape[1]
    
    # Calculate the index of the central column.
    center_col_index = num_cols // 2
    
    # Iterate through the rows of the input grid.
    for row_index in range(input_grid.shape[0]):
        # Get the pixel from the central column of the current row.
        pixel_value = input_grid[row_index, center_col_index]
        
        # Check if the pixel is non-white (not 0).
        if pixel_value != 0:
            # Place the pixel in the output grid at the same row and central column.
            output_grid[row_index, center_col_index] = pixel_value
            
    return output_grid
```
