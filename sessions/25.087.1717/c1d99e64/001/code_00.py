"""
Identifies rows and columns composed entirely of white pixels (0) in the input grid. 
Changes all pixels within those identified rows and columns to red (2) in the output grid. 
If a pixel is part of both an all-white row and an all-white column, it becomes red. 
Pixels not belonging to an all-white row or column retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all-white rows and columns with red.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier slicing and operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Get grid dimensions
    height, width = input_grid_np.shape
    
    # Define constants for colors
    WHITE = 0
    RED = 2

    # Iterate through each row
    for r in range(height):
        # Check if all pixels in the current row are white (0)
        if np.all(input_grid_np[r, :] == WHITE):
            # If the row is all white, change the corresponding row in the output grid to red (2)
            output_grid[r, :] = RED
            
    # Iterate through each column
    for c in range(width):
        # Check if all pixels in the current column are white (0)
        if np.all(input_grid_np[:, c] == WHITE):
            # If the column is all white, change the corresponding column in the output grid to red (2)
            output_grid[:, c] = RED

    # Return the modified output grid (converted back to list of lists if necessary, 
    # but numpy array is often preferred for ARC tasks)
    return output_grid.tolist() # Convert back to list of lists for standard ARC format if needed