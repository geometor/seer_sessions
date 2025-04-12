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
    
    # Convert the input list of lists to a numpy array for efficient array operations.
    input_array = np.array(input_grid, dtype=int)
    
    # Perform a 180-degree rotation. 
    # np.rot90 rotates counterclockwise 90 degrees. Applying it twice (k=2) results in a 180-degree rotation.
    rotated_array = np.rot90(input_array, k=2)
    
    # Convert the resulting numpy array back to a standard list of lists format for the output.
    output_grid = rotated_array.tolist()
    
    # Return the transformed grid.
    return output_grid