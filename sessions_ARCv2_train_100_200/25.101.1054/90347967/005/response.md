```python
"""
Rotates the input grid by 180 degrees globally around the grid's center. 
Each pixel at input coordinate (r, c) moves to the output coordinate 
(H - 1 - r, W - 1 - c), where H is the height and W is the width of the grid. 
The color of the pixel is preserved. This rule accurately describes the 
transformation for the first two training examples (train_1, train_2). 
Note that the third training example's (train_3) provided output does not 
match the result of this transformation, suggesting an inconsistency or a more 
complex rule not fully captured by the available examples.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies a 180-degree rotation to the entire input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid, rotated 180 degrees.
    """
    # Convert the input list of lists to a numpy array for easier indexing and manipulation.
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions (height H, width W) of the input grid.
    height, width = input_array.shape
    
    # Create a new numpy array for the output grid, initialized with the 
    # background color (0), and having the same dimensions as the input grid.
    # Using zeros_like ensures the output has the same shape and dtype.
    output_array = np.zeros_like(input_array)
    
    # Iterate through each pixel of the input grid using its row (r) and column (c) indices.
    for r in range(height):
        for c in range(width):
            # Retrieve the color value of the pixel at the current input coordinates (r, c).
            pixel_value = input_array[r, c]
            
            # Calculate the target coordinates (target_r, target_c) in the output grid 
            # corresponding to a 180-degree rotation relative to the grid's center.
            # The target row is found by reflecting the current row across the horizontal midline.
            target_r = height - 1 - r
            # The target column is found by reflecting the current column across the vertical midline.
            target_c = width - 1 - c
            
            # Place the retrieved pixel value into the calculated target coordinates of the output grid.
            output_array[target_r, target_c] = pixel_value
            
    # Convert the resulting numpy array back to a standard list of lists format for the output.
    output_grid = output_array.tolist()
    
    # Return the transformed grid.
    return output_grid
```