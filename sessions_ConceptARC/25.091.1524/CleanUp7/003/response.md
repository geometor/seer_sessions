```python
"""
Replace all azure (8) pixels with white (0) pixels. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all azure (8) pixels with white (0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify and return as the output
    output_grid = np.copy(grid)
    
    # Find the coordinates (rows and columns) of all pixels with the color azure (8)
    azure_coords = np.where(grid == 8)
    
    # Replace the pixels at the identified coordinates with white (0) in the output grid
    output_grid[azure_coords] = 0
    
    # Convert the modified NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()

```