```python
"""
The input grid (excluding the last all-zero column) is doubled in both dimensions to form the output. 
The output grid's final two columns reflect the last non-zero column, plus added 0's for the final color.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)
    
    # Get dimensions of input grid, excluding the last column
    rows, cols = input_array.shape
    cols -= 1  # Exclude the last column

    # Initialize output grid with double the dimensions (excluding the zero column)
    output_array = np.zeros((rows * 2, cols * 2), dtype=int)

    # Replicate the input grid (excluding the last column)
    for i in range(rows):
        for j in range(cols):
            color = input_array[i, j]
            output_array[2*i:2*i+2, 2*j:2*j+2] = color

    # Get the last non-zero column from the input
    last_non_zero_col = input_array[:, cols-1]

    # Fill the last two columns of the output based on last_non_zero_col
    for i in range(rows):
      output_array[2*i:2*i+2, 2*cols-2:2*cols] = last_non_zero_col[i]
      
    # Fill in 0 for the last color.
    last_color = input_array[-1,-2] # second to last column, bottom row.
    
    for i in range(rows):
      if(input_array[i,-2] == last_color):
        output_array[2*i:2*i+2, 2*cols-2:2*cols] = last_non_zero_col[i]
    
    # Find where we need 0s for the last color
    
    for i in range(rows):
      if (last_non_zero_col[i] == last_color):
         k = i
    
    output_array[2*k:, 2*cols-2:2*cols] = 0
    
    

    return output_array.tolist()
```