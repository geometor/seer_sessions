"""
Identify the unique white pixel in the input grid. Change the color of all pixels that lie on the two main diagonals passing through this original white pixel to white (0). All other pixels retain their original color from the input grid.
"""

import numpy as np

def find_unique_pixel_coords(grid_array, color):
    """
    Finds the coordinates of the unique pixel with the specified color.
    Raises ValueError if zero or more than one pixel of that color is found.
    """
    coords = np.where(grid_array == color)
    if len(coords[0]) == 0:
        raise ValueError(f"No pixel with color {color} found in the input grid.")
    if len(coords[0]) > 1:
        # Although the examples suggest only one, handle potential variations robustly.
        # For this specific task, we expect exactly one.
        raise ValueError(f"Multiple pixels with color {color} found. Expected exactly one.")
        # Alternative for flexibility: print("Warning: Multiple pixels found. Using the first one.")
        # return coords[0][0], coords[1][0] 
        
    return coords[0][0], coords[1][0]

def transform(input_grid):
    """
    Transforms the input grid by setting pixels to white if they lie on the
    diagonals passing through the original unique white pixel.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Find the coordinates (r0, c0) of the unique white pixel (value 0)
    try:
        r0, c0 = find_unique_pixel_coords(input_array, 0)
    except ValueError as e:
        # Handle cases where the assumption of one white pixel is violated
        print(f"Error processing grid: {e}")
        # Depending on requirements, could return input_grid, None, or raise the error
        raise e 

    # Initialize the output grid as a copy of the input grid
    # Pixels not matching the condition will retain their original color
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Calculate the absolute difference in rows and columns from the original white pixel
            delta_row = abs(r - r0)
            delta_col = abs(c - c0)
            
            # Check if the pixel lies on one of the diagonals passing through (r0, c0)
            # This condition (abs(r - r0) == abs(c - c0)) defines the diagonals
            if delta_row == delta_col:
                # If it's on a diagonal, set the corresponding pixel in the output grid to white (0)
                output_array[r, c] = 0
            # If not on a diagonal, the pixel retains its original color (already handled by copying)

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
