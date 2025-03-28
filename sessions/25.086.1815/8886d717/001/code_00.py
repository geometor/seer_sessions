"""
Modify the grid by changing specific orange (7) pixels to azure (8) if their immediate left neighbor is azure (8).
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each row of the grid.
3. Within each row, iterate through each column starting from the second column (index 1).
4. Check if the pixel to the immediate left (row, col-1) is azure (8) and the current pixel (row, col) is orange (7).
5. If both conditions are true, change the current pixel in the output grid to azure (8).
6. Otherwise, the pixel retains its original color from the input grid.
7. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each row
    for r in range(height):
        # Iterate through each column, starting from the second column (index 1)
        # because we need to check the left neighbor
        for c in range(1, width):
            # Check the condition: left neighbor is azure (8) and current pixel is orange (7)
            if input_array[r, c - 1] == 8 and input_array[r, c] == 7:
                # Change the current pixel in the output grid to azure (8)
                output_grid[r, c] = 8
                
    return output_grid.tolist() # Return as list of lists as per common ARC format