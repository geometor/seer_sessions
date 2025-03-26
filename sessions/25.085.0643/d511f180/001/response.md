```python
"""
Iterate through each pixel of the input grid. If a pixel's color is gray (5), 
change it to azure (8) in the output grid. If a pixel's color is azure (8), 
change it to gray (5) in the output grid. Otherwise, keep the pixel's color 
the same in the output grid. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping gray (5) and azure (8) pixels.

    Args:
        input_grid (list of lists of int): The input grid represented as a 2D list.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Convert the input list of lists to a NumPy array for efficient element-wise operations
    np_input = np.array(input_grid, dtype=int)
    
    # Create a copy of the input array to modify, which will become the output grid
    # This ensures pixels not matching the conditions remain unchanged
    np_output = np_input.copy()

    # Identify the locations of gray (5) pixels
    is_gray = (np_input == 5)
    
    # Identify the locations of azure (8) pixels
    is_azure = (np_input == 8)
    
    # Change gray pixels (5) to azure (8) in the output grid
    np_output[is_gray] = 8
    
    # Change azure pixels (8) to gray (5) in the output grid
    np_output[is_azure] = 5

    # Convert the resulting NumPy array back to a list of lists format
    output_grid = np_output.tolist()

    return output_grid

```