```python
"""
The transformation mirrors the input grid both horizontally and vertically.
This is equivalent to rotating the grid 180 degrees. The color values are preserved.
Input[i, j] maps to Output[height - 1 - i, width - 1 - j]
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring it both horizontally and vertically.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
    
    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Get the height and width of the grid
    height, width = input_array.shape
    
    # Initialize the output grid with zeros
    output_array = np.zeros_like(input_array)
    
    # Iterate through the input grid and map each element to its new position in the output grid
    for i in range(height):
        for j in range(width):
            output_array[height - 1 - i, width - 1 - j] = input_array[i, j]
    
    # Convert the output array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
```