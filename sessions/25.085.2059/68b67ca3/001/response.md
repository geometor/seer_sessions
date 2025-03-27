```python
"""
Takes a 6x6 input grid and produces a 3x3 output grid by selecting pixels 
from the input grid at even row and even column indices. Specifically, 
the pixel at output coordinate (r_out, c_out) is copied from the input 
grid coordinate (r_out * 2, c_out * 2).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by subsampling every second pixel 
    starting from the top-left corner (0,0).
    
    Args:
        input_grid (list of lists): The input grid.
        
    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    input_height, input_width = input_array.shape
    
    # Calculate output dimensions (integer division)
    output_height = input_height // 2
    output_width = input_width // 2
    
    # Create the output grid by selecting elements at even indices
    # Start at index 0, go up to the end, step by 2 for both rows and columns
    output_grid = input_array[0:input_height:2, 0:input_width:2]
    
    return output_grid

```