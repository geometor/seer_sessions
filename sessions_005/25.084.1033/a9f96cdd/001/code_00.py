import numpy as np

"""
Place four specific colors (green=3, magenta=6, azure=8, orange=7) diagonally 
adjacent to the position of the single input red pixel (2), if the target 
positions fall within the grid boundaries. The original red pixel location 
becomes white (0) in the output.
"""

def find_pixel_coordinates(grid, color_value):
    """
    Finds the coordinates (row, col) of the first pixel with the specified color_value.
    Returns None if the pixel is not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_value:
                return r, c
    return None # Should not happen based on task description

def is_within_bounds(grid, row, col):
    """
    Checks if the given coordinates (row, col) are within the grid boundaries.
    """
    rows, cols = grid.shape
    return 0 <= row < rows and 0 <= col < cols

def transform(input_grid):
    """
    Transforms the input grid based on the position of the red pixel.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions as input, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # Locate the coordinates (R, C) of the single red pixel (2)
    red_coord = find_pixel_coordinates(input_np, 2)
    if red_coord is None:
        # If no red pixel is found (unexpected based on examples), return the empty grid
        return output_grid.tolist() 
        
    R, C = red_coord

    # Define the four target relative positions and their corresponding colors
    # (dr, dc, color)
    targets = [
        (-1, -1, 3),  # Green
        (-1, +1, 6),  # Magenta
        (+1, -1, 8),  # Azure
        (+1, +1, 7)   # Orange
    ]

    # Iterate through the target definitions
    for dr, dc, color in targets:
        # Calculate the absolute target coordinates
        target_row = R + dr
        target_col = C + dc

        # Check if the target coordinates are within the grid bounds
        if is_within_bounds(output_grid, target_row, target_col):
            # If within bounds, place the corresponding color in the output grid
            output_grid[target_row, target_col] = color

    # Return the final output grid as a list of lists
    return output_grid.tolist()