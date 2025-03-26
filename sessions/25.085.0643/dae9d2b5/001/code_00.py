"""
Transforms an input grid based on a comparison between its left and right halves.

1. Determine the dimensions of the input grid (Height H, Width W). The output grid will have dimensions Height H, Width W/2.
2. Create a new grid for the output, initialized with white (0), matching the output dimensions.
3. Iterate through each cell of the output grid using its row index `i` (from 0 to H-1) and column index `j` (from 0 to W/2 - 1).
4. For the current cell `(i, j)` in the output grid:
    a. Identify the corresponding cell in the left half of the input grid at `(i, j)`. Let its color be `left_color`.
    b. Identify the corresponding cell in the right half of the input grid at `(i, j + W/2)`. Let its color be `right_color`.
    c. Check if `left_color` is yellow (4) or if `right_color` is green (3).
    d. If the condition in step 4c is true, set the output grid cell at `(i, j)` to magenta (6).
    e. Otherwise (if `left_color` is not yellow (4) and `right_color` is not green (3)), leave the output grid cell at `(i, j)` as white (0).
5. Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Determine input dimensions
    height, width = input_array.shape
    
    # Calculate the width of the output grid (half of the input width)
    output_width = width // 2
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((height, output_width), dtype=int)
    
    # Iterate through each cell of the conceptual output grid
    for i in range(height):
        for j in range(output_width):
            # Get the color from the left half of the input grid
            left_color = input_array[i, j]
            
            # Get the color from the right half of the input grid
            # The corresponding column index in the right half is j + output_width
            right_color = input_array[i, j + output_width]
            
            # Apply the transformation rule:
            # If the left pixel is yellow (4) OR the right pixel is green (3)
            if left_color == 4 or right_color == 3:
                # Set the corresponding output pixel to magenta (6)
                output_grid[i, j] = 6
            # Otherwise, the output pixel remains white (0) as initialized
                
    return output_grid
