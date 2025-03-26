```python
"""
This program transforms an input grid by extracting only its central vertical column. 
All other columns are replaced with white pixels (0). The central column index is 
determined by floor((width - 1) / 2).
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the central column of the input grid and sets all other pixels to white (0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid with only the central column preserved.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions (height and width) of the input grid
    height, width = input_np.shape
    
    # Calculate the index of the central column
    # Using integer division // automatically handles the floor operation
    center_column_index = (width - 1) // 2
    
    # Create a new output grid with the same dimensions as the input, 
    # initialized with white pixels (0)
    output_np = np.zeros_like(input_np)
    
    # Iterate through each row of the input grid
    for r in range(height):
        # Get the pixel value from the input grid at the center column for the current row
        pixel_value = input_np[r, center_column_index]
        
        # Set the corresponding pixel in the output grid's center column to this value
        output_np[r, center_column_index] = pixel_value
        
    # Convert the NumPy array back to a list of lists for the final output format
    output_grid = output_np.tolist()
    
    return output_grid

```