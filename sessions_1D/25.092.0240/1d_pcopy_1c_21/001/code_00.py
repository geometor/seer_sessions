import numpy as np

"""
Expand single non-white pixels into 1x3 horizontal lines of the same color, 
centered at the original pixel's position. Leave all other non-white shapes 
and the white background unchanged.
"""

def is_single_pixel(grid, r, c):
    """
    Checks if the pixel at (r, c) is a non-white pixel with no 
    adjacent non-white neighbors horizontally or vertically.
    Handles boundary conditions.
    """
    height, width = grid.shape
    color = grid[r, c]

    # Must be non-white
    if color == 0:
        return False

    # Check neighbors (within bounds)
    # Up
    if r > 0 and grid[r - 1, c] == color:
        return False
    # Down
    if r < height - 1 and grid[r + 1, c] == color:
        return False
    # Left
    if c > 0 and grid[r, c - 1] == color:
        return False
    # Right
    if c < width - 1 and grid[r, c + 1] == color:
        return False

    # If no adjacent neighbors have the same color, it's a single pixel object
    return True

def transform(input_grid):
    """
    Transforms the input grid by expanding single non-white pixels into 
    1x3 horizontal lines, keeping other elements the same.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is a single non-white pixel
            if is_single_pixel(input_array, r, c):
                color = input_array[r, c]
                
                # Expand into a 1x3 horizontal line in the output grid
                # The center pixel (r, c) is already correct due to the copy
                
                # Set left pixel if within bounds
                if c > 0:
                    output_array[r, c - 1] = color
                
                # Set right pixel if within bounds
                if c < width - 1:
                    output_array[r, c + 1] = color

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    return output_grid
