```python
import numpy as np

"""
Rotates the input grid by 180 degrees around its center. Each pixel at input 
coordinate (r, c) moves to the output coordinate (H - 1 - r, W - 1 - c), 
where H is the height and W is the width of the grid. The color of the pixel 
is preserved. This rule accurately describes the transformation for the first 
two training examples. Note that the third training example's provided output 
does not match the result of this transformation.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a 180-degree rotation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid, rotated 180 degrees.
    """
    # Convert the input list of lists to a numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions (height H, width W) of the input grid
    height, width = input_array.shape
    
    # Create a new numpy array for the output grid, initialized with the 
    # background color (0), and having the same dimensions as the input grid
    output_array = np.zeros_like(input_array)
    
    # Iterate through each pixel of the input grid using its row (r) and column (c) indices
    for r in range(height):
        for c in range(width):
            # Retrieve the color value of the pixel at the current input coordinates (r, c)
            pixel_value = input_array[r, c]
            
            # Calculate the target coordinates (target_r, target_c) in the output grid 
            # corresponding to a 180-degree rotation.
            # The new row index is calculated by subtracting the current row index from the last row index (height - 1).
            target_r = height - 1 - r
            # The new column index is calculated by subtracting the current column index from the last column index (width - 1).
            target_c = width - 1 - c
            
            # Place the retrieved pixel value into the calculated target coordinates of the output grid
            output_array[target_r, target_c] = pixel_value
            
    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_array.tolist()
    
    # Return the transformed grid
    return output_grid
```